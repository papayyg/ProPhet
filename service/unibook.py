import json
import os
import re
import asyncio

import aiohttp
from bs4 import BeautifulSoup as BS

from locales.translations import _
from utils.locales import locales_dict

from data.config import secret_login, secret_password

link = 'http://lms.adnsu.az/adnsuEducation/cs'

async def faculty(session):
    faculty_data = {
        'action': 'getComboContent',
        'comboType': '3',
        'filterNo': '1',
        'orgTypeId': '1000002',
    }
    request = await session.post(link, data=faculty_data)
    faculty_request = await request.text()
    return json.loads(faculty_request)['data'][0]['id']

async def logpass(text):
    login = text[text.find(' ') + 1:text.find(' ', text.find(' ') + 1)]
    password = text[text.find(' ', text.find(' ') + 1) + 1:]
    return login, password

async def years(session):
    years = {
        'action': 'getComboContent',
        'comboType': '1000006-edu-year',
        'filterNo': '-1'
    }
    request = await session.post(link, data=years)
    years_request = await request.text()
    return json.loads(years_request)['data'][-1]['id']


async def sem(session, year_id):
    sem = {
        'action': 'getComboContent',
        'comboType': '1000006-3',
        'filterNo': '-1',
        'edu_year_id': year_id
    }
    request = await session.post(link, data=sem)
    sem_request = await request.text()
    return json.loads(sem_request)['data'][-1]['id']


async def group(session):
    faculty_id = await faculty(session)
    group = {
        'action': 'getComboContent',
        'comboType': 'academicGroups',
        'filterNo': '3',
        'orgId': faculty_id,
        'specTypeId': '0',
        'specId': '0',
        'kurs': '0',
    }
    await session.get(f"{link}?action=load&modulId=1000004")
    request = await session.post(link, data=group)
    group_request = await request.text()
    return json.loads(group_request)['data'][0]['group_id']


async def student(session, year_id, group_id):
    student = {
        'action': 'getComboContent',
        'comboType': '4',
        'filterNo': '4',
        'specialityId': '0',
        'eduYearId': year_id,
        'groupId': group_id
    }
    request = await session.post(link, data=student)
    student_request = await request.text()
    return json.loads(student_request)['data'][0]['id'], f"<b>{' '.join(json.loads(student_request)['data'][0]['name'].split()[:2])}</b>\n"\

async def subjects(session, sem_id, student_id, group_id):
    faculty_id = await faculty(session)
    subjects_list = {
        "action": "subjects",
        "sub_action": "loadSubject",
        "semesterId": sem_id,
        "stud_id": student_id,
        "emp_id": "0",
        "facultyId": faculty_id,
        "cafedra_id": "0",
        "groupId": group_id,
        "code": "",
        "count": "21",
        "currentModuleId": "1000004"
    }
    request = await session.post(link, data=subjects_list)
    request_bs = BS(await request.text(), "html.parser")
    items = request_bs.find_all('a', attrs={"data-toggle": "popover"})
    subj_title = request_bs.find_all('p')
    return [item.text.strip() for item in subj_title], [item['data-subj-id'] for item in items]

async def journal_qb(session, subjects_id, subj_title):
    result = {}
    for i in range(len(subjects_id)):
        journal = {
            'action': 'subjects',
            'sub_action': 'getSubjectResultJournal',
            'subj_id': subjects_id[i]
        }
        count = {
            'action': 'subjects',
            'sub_action': 'getSubjectJournal',
            'subj_id': subjects_id[i],
            'pageNum': 1
        }
        final = {
            'action': 'getComboContent',
            'comboType': 'getSubTeacherList',
            'filterNo': '-1',
            'subjectId': subjects_id[i]
        }
        request = await session.post(link, data=journal)
        request_count = await session.post(link, data=count)
        request_final = await session.post(link, data=final)
        request_bs = BS(await request.text(), "html.parser")
        count_bs = BS(await request_count.text(), "html.parser")
        final_request = await request_final.text()
        final_hours = json.loads(final_request)['additionalData']['3'][0]
        hours = int((int(final_hours['l_hours']) +
                     int(final_hours['m_hours']) + int(final_hours['s_hours'])) * 25 / 100 / 2)
        qb_count = 0
        while len(count_bs.select("tbody > tr > td")) > 2:
            for a in count_bs.select("tbody > tr > td > span.label"):
                if 'q.' in a and 'məq.' not in a:
                    qb_count += 1
            count['pageNum'] += 1
            request_count = await session.post(link, data=count)
            count_bs = BS(await request_count.text(), "html.parser")
        if len(request_bs.select("tbody > tr > td")) != 0:
            qb = request_bs.select("tbody > tr > td")[3].text
            if qb_count < hours*20/100:
                smile = '🔵'
            elif qb_count < hours*40/100:
                smile = '🟢'
            elif qb_count < hours*60/100:
                smile = '🟡'
            elif qb_count < hours*80/100:
                smile = '🟠'
            elif qb_count <= hours:
                smile = '🔴'
            elif qb_count > hours:
                smile = '❌'
            else:
                smile = '⚪️'
        else:
            smile = '⚪️'
            qb = '-'
        result[subjects_id[i]] = [f'{smile} <b>{qb_count}/{hours}</b>',
                                  subj_title[i].rstrip('.'), f'<i>{qb}%</i>']
    return result

async def miss(username, password):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": username,
            "password": password
        }
        await session.post(
            "http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        year_id = await years(session)
        sem_id = await sem(session, year_id)
        group_id = await group(session)
        student_id, student_name = await student(session, year_id, group_id)
        subj_title, subjects_id = await subjects(
            session, sem_id, student_id, group_id)
        result = await journal_qb(session, subjects_id, subj_title)
        t = student_name
        for i in result:
            t += f'{result[i][0]} {result[i][1]}: {result[i][2]}\n'
    return t

async def try_auth(login, password):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": login,
            "password": password
        }
        response = await session.post("http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        if 'Daxil ol' not in await response.text(): return True
        else: return False


async def summarys(username, password, chat_id):
    result = await _('<b>Все предметы:</b>\n\n', locales_dict[chat_id])
    summary_credit = 0
    total = 0
    temp_total = 0
    temp_credit = 0
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": username,
            "password": password
        }
        await session.post(
            "http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        years = {
            'action': 'getComboContent',
            'comboType': '1000006-edu-year',
            'filterNo': '-1'
        }
        request = await session.post(link, data=years)
        years_request = await request.text()
        group_id = await group(session)
        for year_id in reversed(json.loads(years_request)['data']):
            sem = {
                'action': 'getComboContent',
                'comboType': '1000006-3',
                'filterNo': '-1',
                'edu_year_id': year_id['id']
            }
            request = await session.post(link, data=sem)
            sem_request = await request.text()
            student_id, student_name = await student(session, year_id['id'], group_id)
            for sem_id in json.loads(sem_request)['data']:
                sem_point = 0
                sem_credit = 0
                subj_title, subjects_id = await subjects(session, sem_id['id'], student_id, group_id)
                for subj_id in subjects_id:
                    info_data = {
                        'action': 'getComboContent',
                        'comboType': 'getSubTeacherList',
                        'filterNo': '-1',
                        'subjectId': subj_id
                    }
                    request = await session.post(link, data=info_data)
                    info_request = await request.text()
                    info_3 = json.loads(info_request)['additionalData']['3'][0]
                    subj_title = info_3['subname'][info_3['subname'].find('>') + 2:]
                    credit = info_3['credit']
                    journal = {
                        'action': 'subjects',
                        'sub_action': 'getSubjectResultJournal',
                        'subj_id': subj_id
                    }
                    request = await session.post(link, data=journal)
                    response = BS(await request.text(), "html.parser")
                    mark_list = []
                    if len(response.select("tbody > tr > td")) != 0:
                        for el in response.select("tbody > tr"):
                            item = el.select("td")
                            for i in range(2, len(item)):
                                point = item[i].text.strip()
                                mark_list.append(point)
                    if mark_list != []:
                        if mark_list[11] != '':
                            final_point = mark_list[11]

                        else:
                            final_point = mark_list[9]
                        if mark_list[11] == mark_list[9] and mark_list[10] not in ['-', '0']:
                            final_point = int(mark_list[9]) + int(mark_list[10])
                    else:
                        final_point = '0'
                    if int(final_point) < 51:
                        result += '❗️'
                        summary_credit += int(credit)
                        total += int(credit) * int(final_point)
                    else:
                        summary_credit += int(credit)
                        total += int(credit) * int(final_point)
                        temp_total += int(final_point) * int(credit)
                        temp_credit += int(credit)
                    sem_point += int(credit) * int(final_point)
                    sem_credit += int(credit)
                    credit = info_3['credit']
                    result += f'<i>{subj_title}</i>: <b>{final_point} {credit}</b>\n'
                if sem_credit != 0:
                    temp_text = await _('✅ <b><i>Средний балл за семестр: {sredniy} ({sem_point} {sem_credit})</i></b>\n\n', locales_dict[chat_id])
                    result += temp_text.format(sredniy=round(sem_point / sem_credit, 3), sem_point=sem_point, sem_credit=sem_credit)
        if '❗️' in result:
            temp_text = await _('🎓\nИтоговый средний балл: {sredniy}\nСумма баллов: {total}\nСумма кредитов: {summary_credit}\n\nСредний балл без учета проблемных: {sredniy_p}\nСумма баллов: {temp_total}\nСумма кредитов: {temp_credit}', locales_dict[chat_id])
            result += temp_text.format(sredniy=round(total / summary_credit, 3), total=total, summary_credit=summary_credit, sredniy_p=round(temp_total / temp_credit, 3), temp_total=temp_total, temp_credit=temp_credit)
        else:
            temp_text = await _('🎓\nИтоговый средний балл: {sredniy}\nСумма баллов: {total}\nСумма кредитов: {summary_credit}', locales_dict[chat_id])
            result += temp_text.format(sredniy=round(total / summary_credit, 3), total=total, summary_credit=summary_credit)
    return result

async def summary(username, password, chat_id):
    result = ''
    summary_credit = 0
    total = 0
    temp_total = 0
    temp_credit = 0
    s = 0
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": username,
            "password": password
        }
        await session.post(
            "http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        years = {
            'action': 'getComboContent',
            'comboType': '1000006-edu-year',
            'filterNo': '-1'
        }
        request = await session.post(link, data=years)
        years_request = await request.text()
        group_id = await group(session)
        for year_id in reversed(json.loads(years_request)['data']):
            sem = {
                'action': 'getComboContent',
                'comboType': '1000006-3',
                'filterNo': '-1',
                'edu_year_id': year_id['id']
            }
            request = await session.post(link, data=sem)
            sem_request = await request.text()
            student_id, student_name = await student(session, year_id['id'], group_id)
            for sem_id in json.loads(sem_request)['data']:
                subj_title, subjects_id = await subjects(session, sem_id['id'], student_id, group_id)
                for subj_id in subjects_id:
                    info_data = {
                        'action': 'getComboContent',
                        'comboType': 'getSubTeacherList',
                        'filterNo': '-1',
                        'subjectId': subj_id
                    }
                    request = await session.post(link, data=info_data)
                    info_request = await request.text()
                    info_3 = json.loads(info_request)['additionalData']['3'][0]
                    subj_title = info_3['subname'][info_3['subname'].find('>') + 2:]
                    credit = info_3['credit']
                    journal = {
                        'action': 'subjects',
                        'sub_action': 'getSubjectResultJournal',
                        'subj_id': subj_id
                    }
                    request = await session.post(link, data=journal)
                    response = BS(await request.text(), "html.parser")
                    mark_list = []
                    if len(response.select("tbody > tr > td")) != 0:
                        for el in response.select("tbody > tr"):
                            item = el.select("td")
                            for i in range(2, len(item)):
                                point = item[i].text.strip()
                                mark_list.append(point)
                    if mark_list != []:
                        if mark_list[11] != '':
                            final_point = mark_list[11]

                        else:
                            final_point = mark_list[9]
                        if mark_list[11] == mark_list[9] and mark_list[10] not in ['-', '0']:
                            final_point = int(mark_list[9]) + int(mark_list[10])
                    else:
                        final_point = '0'
                    if int(final_point) < 51:
                        summary_credit += int(credit)
                        total += int(credit) * int(final_point)
                        s = 1
                    else:
                        summary_credit += int(credit)
                        total += int(credit) * int(final_point)
                        temp_total += int(final_point) * int(credit)
                        temp_credit += int(credit)
                    credit = info_3['credit']
        if s == 1:
            temp_text = await _('🎓\nИтоговый средний балл: {sredniy}\nСумма баллов: {total}\nСумма кредитов: {summary_credit}\n\nСредний балл без учета проблемных: {sredniy_p}\nСумма баллов: {temp_total}\nСумма кредитов: {temp_credit}', locales_dict[chat_id])
            result += temp_text.format(sredniy=round(total / summary_credit, 3), total=total, summary_credit=summary_credit, sredniy_p=round(temp_total / temp_credit, 3), temp_total=temp_total, temp_credit=temp_credit)
        else:
            temp_text = await _('🎓\nИтоговый средний балл: {sredniy}\nСумма баллов: {total}\nСумма кредитов: {summary_credit}', locales_dict[chat_id])
            result += temp_text.format(sredniy=round(total / summary_credit, 3), total=total, summary_credit=summary_credit)
    return result

async def journal_full(session, subjects_id, subj_title, student_name, chat_id):
    result_list = {}
    output = []
    for id in range(len(subjects_id)):
        journal = {
                    'action': 'subjects',
                    'sub_action': 'getSubjectResultJournal',
                    'subj_id': subjects_id[id]
                }
        request = await session.post(link, data=journal)
        response = BS(await request.text(), "html.parser")
        mark_list = []
        if len(response.select("tbody > tr > td")) != 0:
            for el in response.select("tbody > tr"):
                item = el.select("td")
                for i in range(2, len(item)):
                    point = item[i].text.strip()
                    mark_list.append(point)
            result_list[subjects_id[id]] = [subj_title[id], mark_list]
            temp = f'👤 {student_name}\n📚 <b>{subj_title[id].rstrip(".")}</b>\n'
            if mark_list[3] != '-':
                temp_text = await _('Cамостоятельная работа: <i>{mark}</i>\n', locales_dict[chat_id])
                temp += temp_text.format(mark=mark_list[3])
            if mark_list[4] != '-':
                temp_text = await _('Презентация: <i>{mark}</i>\n', locales_dict[chat_id])
                temp += temp_text.format(mark=mark_list[4])
            if mark_list[5] != '-':
                temp_text = await _('Курсовая работа: <i>{mark}</i>\n', locales_dict[chat_id])
                temp += temp_text.format(mark=mark_list[5])
            if mark_list[6] != '-':
                temp_text = await _('Лабораторная: <i>{mark}</i>\n', locales_dict[chat_id])
                temp += temp_text.format(mark=mark_list[6])
            if mark_list[7] != '-':
                temp_text = await _('Квиз: <i>{mark}</i>\n', locales_dict[chat_id])
                temp += temp_text.format(mark=mark_list[7])
            if mark_list[8] != '-':
                temp_text = await _('Мидтерм: <i>{mark}</i>\n', locales_dict[chat_id])
                temp += temp_text.format(mark=mark_list[8])
            if mark_list[10] == '':
                mark_list[10] = await _('Еще не был', locales_dict[chat_id])
            if mark_list[11] == '':
                mark_list[11] = await _('После экзамена', locales_dict[chat_id])

            temp_text = await _('Балл до экзамена: <i>{mark_9}</i>\nЭкзамен: <i>{mark_10}</i>\nИтоговый балл (Буква): <i>{mark_11} {mark_12}</i>\nНБ: <i>{mark_1}%</i>\n', locales_dict[chat_id])
            temp += temp_text.format(mark_9=mark_list[9], mark_10=mark_list[10], mark_11=mark_list[11], mark_12=mark_list[12], mark_1=mark_list[1])
            output.append(temp)
    return output

async def full_info(username, password, chat_id):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": username,
            "password": password
        }
        await session.post(
            "http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        year_id = await years(session)
        sem_id = await sem(session, year_id)
        group_id = await group(session)
        student_id, student_name = await student(session, year_id, group_id)
        subj_title, subjects_id = await subjects(session, sem_id, student_id, group_id)
        return await journal_full(session, subjects_id, subj_title, student_name, chat_id)

async def get_files(session, subj_id, output_files, obj_files, chat_id):
    files_info = {'action': 'getModuleContent',
                    'moduleId': '1000062',
                    'topicId': '0',
                    'subjectId': subj_id}
    request = await session.post(link, data=files_info)
    files_request = await request.text()
    temp_files = []
    for el in json.loads(files_request)['data']:
            file_id = el['file_id'].replace(' ', '')
            name = el['topic_name']
            if locales_dict[chat_id] == 'ru':
                if name == "Sillabus-passiv":
                    name = 'Пассивный силлабус 📑'
                elif name == "Sillabus":
                    name = "Силлабус 📟"
                elif name == "Təqdimat":
                    name = "Темы презентаций 💿"
                elif name == "Əlavə vəsaitlər":
                    name = "Дополнительные материалы 🗃"
                elif name == "Mühazirə":
                    name = "Лекции 🗑"
            temp_files.append([file_id, name])
            obj_files[int(file_id)] = name
    output_files.append(temp_files)
    return output_files, obj_files

async def subjects_info(username, password, chat_id):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": username,
            "password": password}

        await session.post(
            "http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        year_id = await years(session)
        sem_id = await sem(session, year_id)
        group_id = await group(session)
        student_id, student_name = await student(session, year_id, group_id)
        subj_title, subjects_id = await subjects(session, sem_id, student_id, group_id)
        subjects_list= []
        output_files = []
        obj_files = {}
        for subj_id in subjects_id:
            info_data = {
                'action': 'getComboContent',
                'comboType': 'getSubTeacherList',
                'filterNo': '-1',
                'subjectId': subj_id
            }
            output_files, obj_files = await get_files(session, subj_id, output_files, obj_files, chat_id)
            request = await session.post(link, data=info_data)
            info_request = await request.text()
            info_3 = json.loads(info_request.encode('utf-8'))['additionalData']['3'][0]
            mark = json.loads(info_request)['additionalData']['4'][0]
            subj_title = info_3['subname'][info_3['subname'].find('>')+2:]
            credit = info_3['credit']
            m_hours, s_hours, l_hours = int(info_3['m_hours']), int(info_3['s_hours']), int(info_3['l_hours'])
            temp_hours = await _('<b>{hours}</b> (Лекции: <b>{m_hours}</b>', locales_dict[chat_id])
            hours = temp_hours.format(hours=m_hours+s_hours+l_hours, m_hours=m_hours)
            if s_hours != 0:
                temp_hours = await _(', Семинары: <b>{s_hours}</b>', locales_dict[chat_id])
                hours += temp_hours.format(s_hours=s_hours)
            if l_hours != 0:
                temp_hours = await _(', Лабораторные: <b>{l_hours}</b>', locales_dict[chat_id])
                hours += temp_hours.format(l_hours=l_hours)
            temp_points = await _('Экзамен (<b>{mark}</b>)', locales_dict[chat_id])
            points = temp_points.format(mark=mark["e_i"])
            if mark['midterm'] != '0':
                points += f', Midterm (<b>{mark["midterm"]}</b>)'
            if mark['ki'] != '0':
                temp_points = await _(', Курсовая (<b>{mark}</b>)', locales_dict[chat_id])
                points += temp_points.format(mark=mark["ki"])
            if mark['e_l'] != '0':
                temp_points = await _(', Лабораторные (<b>{mark}</b>)', locales_dict[chat_id])
                points += temp_points.format(mark=mark["e_l"])
            if mark['presentation'] != '0':
                temp_points = await _(', Презентация (<b>{mark}</b>)', locales_dict[chat_id])
                points += temp_points.format(mark=mark["presentation"])
            if mark['si'] != '0':
                temp_points = await _(', Самостоятельные (<b>{mark}</b>)', locales_dict[chat_id])
                points += temp_points.format(mark=mark["si"])
            if mark['quiz'] != '0':
                points += f', Quiz (<b>{mark["quiz"]}</b>)'
            teachers = json.loads(info_request)['data']
            professor = ''
            for i in range(len(teachers)):
                type = teachers[i]["les_type"]
                if type == '(M)':
                    teachers[i]["les_type"] = await _('(Лек.)',locales_dict[chat_id])
                elif type == '(S)':
                    teachers[i]["les_type"] = await _('(Сем.)',locales_dict[chat_id])
                elif type == '(L)':
                    teachers[i]["les_type"] = await _('(Лаб.)',locales_dict[chat_id])
                elif type == '(M,S)':
                    teachers[i]["les_type"] = await _('(Лек. и Сем.)',locales_dict[chat_id])
                elif type == '(S,L)':
                    teachers[i]["les_type"] = await _('(Сем. и Лаб.)',locales_dict[chat_id])
                elif type == '(M,L)':
                    teachers[i]["les_type"] = await _('(Лек. и Лаб.)',locales_dict[chat_id])
                elif type == '(M,S,L)':
                    teachers[i]["les_type"] = await _('(Лек., Сем. и Лаб.)',locales_dict[chat_id])
                if i != 0:
                    professor += ', '
                professor += f'{" ".join(teachers[i]["emp_full_name"].split()[:2])} {teachers[i]["les_type"]}'
            subject_temp = await _('{student_name}\n<b><i>{subj_title}</i></b>\n💸 Количество кредитов: <i>{credit}</i>\n⏳ Общие часы: <i>{hours})</i>\n✅ Тип оценки: <i>{points}</i>\n👨‍🏫 Преподаватели: <i>{professor}</i>',locales_dict[chat_id])
            subjects_list.append(subject_temp.format(student_name=student_name,subj_title=subj_title,credit=credit, hours=hours,points=points,professor=professor))
        return subjects_list, output_files, obj_files


async def download_files(file_id, file_name, logpass):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": logpass[0],
            "password": logpass[1]}
        request = await session.post("http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        request_bs = BS(await request.text(), "html.parser")
        string = request_bs.select("[type='text/javascript']")[0].text
        neuron = string[string.find("=") + 3: string.find(";") - 1]
        url = f"http://lms.adnsu.az/adnsuEducation/upl?neuron={neuron}&action=downloadDocument&fileId={file_id}"
        response = await session.get(url)
        folder_name = f'temp/{logpass[0]}'
        file_path = os.path.join(folder_name, file_name)
        os.makedirs(folder_name, exist_ok=True)
        open(file_path, 'wb').write(await response.read())

async def get_all_nb(login, password):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": login,
            "password": password
        }
        await session.post("http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        year_id = await years(session)
        sem_id = await sem(session, year_id)
        group_id = await group(session)
        student_id, student_name = await student(session, year_id, group_id)
        subj_title, subjects_id = await subjects(session, sem_id, student_id, group_id)
        hours = []
        for sbid in subjects_id:
            limit = {
                'action': 'getComboContent',
                'comboType': 'getSubTeacherList',
                'filterNo': '-1',
                'subjectId': sbid
            }
            final_hours = json.loads((await (await session.post(link, data=limit)).text()))['additionalData']['3'][0]
            hours.append(int((int(final_hours['l_hours']) +
                        int(final_hours['m_hours']) + int(final_hours['s_hours'])) * 25 / 100 / 2))
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": secret_login,
            "password": secret_password
        }
        await session.post("http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        final_result = []
        i = 0
        for subj_id in subjects_id:
            data = {
                "action": 'subjects',
                'sub_action': 'getSubjectJournal',
                'subj_id': subj_id,
                'pageNum': 1
            }
            request = await session.post(link, data=data)
            request_bs = BS(await request.text(), "html.parser")
            journal_table = request_bs.find('table', {'id': 'journal'})
            table = journal_table.find_all('tbody')[-1]
            temp_result = {}
            for tr in table.find_all('tr'):
                first_td = tr.find_all('td')[0].getText()
                second_td = ' '.join(tr.find_all('td')[1].getText().replace("  ", " ").split(' ')[:2])
                count = 0
                for td in tr.find_all('td'):
                    span_list = td.select('span')
                    for span in span_list:
                        if 'q.' in span.text and 'məq.' not in span.text:
                            count += 1
                temp_result[f'{first_td}. {second_td}'] = count
            data['pageNum'] = 2
            request = await session.post(link, data=data)
            request_bs = BS(await request.text(), "html.parser")
            while len(request_bs.select_one('tbody > tr > td')) > 2:
                journal_table = request_bs.find('table', {'id': 'journal'})
                table = journal_table.find_all('tbody')[-1]
                for tr in table.find_all('tr'):
                    first_td = tr.find_all('td')[0].getText()
                    second_td = ' '.join(tr.find_all('td')[1].getText().replace("  ", " ").split(' ')[:2])
                    count = 0
                    for td in tr.find_all('td'):
                        span_list = td.select('span')
                        for span in span_list:
                            if 'q.' in span.text and 'məq.' not in span.text:
                                count += 1
                    temp_result[f'{first_td}. {second_td}'] = temp_result[f'{first_td}. {second_td}'] + count
                data['pageNum'] += 1
                request = await session.post(link, data=data)
                request_bs = BS(await request.text(), "html.parser")
            qb_string = f'<i><b>{subj_title[i]}</b></i>\n'
            for key, value in temp_result.items():
                if value < hours[i]*20/100:
                    smile = '🔵'
                elif value < hours[i]*40/100:
                    smile = '🟢'
                elif value < hours[i]*60/100:
                    smile = '🟡'
                elif value < hours[i]*80/100:
                    smile = '🟠'
                elif value <= hours[i]:
                    smile = '🔴'
                elif value > hours[i]:
                    smile = '❌'
                else:
                    smile = '⚪️'
                string = f'{smile} {key}: <i>{value}/{hours[i]}</i>\n'
                qb_string += string
            final_result.append(qb_string)
            i += 1
    return final_result

async def get_all_journal(login, password, chat_id):
    async with aiohttp.ClientSession() as session:
        payload = {
            "username": login,
            "password": password
        }
        await session.post("http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        year_id = await years(session)
        sem_id = await sem(session, year_id)
        group_id = await group(session)
        student_id, student_name = await student(session, year_id, group_id)
        subj_title, subjects_id = await subjects(session, sem_id, student_id, group_id)
    async with aiohttp.ClientSession() as session:
        student_data = []
        payload = {
            "username": secret_login,
            "password": secret_password
        }
        final_result = []
        await session.post("http://lms.adnsu.az/adnsuEducation/ls?action=login", data=payload)
        data = {
                    "action": 'academicGroupOperations',
                    'sub_action': 'loadAcademicGroup',
                    'groupId': group_id,
                }
        request = await session.post(link, data=data)
        request_bs = BS(await request.text(), "html.parser")
        tr_elements = request_bs.find(class_='panel').find(class_='panel-body').find(class_='table-responsive').find('table').find('tbody').find_all('tr')
        for element in tr_elements:
            ths = element.find_all('th')
            student_data.append(' '.join(ths[2].get_text(strip=True).replace("  ", " ").split(' ')[:2]))
        types = ['1200', '1201', '1202', '1204', '1205', '1206']
        modules = ['1000094', '1000092', '1000093', '1000095', '1000108', '1000109']
        j = 0
        for subj_id in subjects_id:
            student_scores = {}
            for item in student_data:
                student_scores[item] = []
            for type_id, module_id in zip(types, modules):
                data = {
                    "action": 'subjects',
                    'sub_action': 'checkSubjectFreeWork',
                    'subjectId': subj_id,
                    'typeId': type_id
                }
                request = await session.post(link, data=data)
                request_bs = BS(await request.text(), "html.parser")
                if request_bs.getText() == '1':
                    data = {
                        "action": 'subjects',
                        'sub_action': 'loadSubjectWorkList',
                        'subjectId': subj_id,
                        'typeId': type_id,
                        'moduleId': module_id
                    }
                    request = await session.post(link, data=data)
                    request_bs = BS(await request.text(), "html.parser")

                    tr_elements = request_bs.find(id='subject-work-journal').find(id='sub_work_journal').find('tbody').find_all('tr')
                    for element in tr_elements:
                        tds = element.find_all('td')
                        name = ' '.join(tds[1].get_text(strip=True).replace("  ", " ").split(' ')[:2])
                        student_scores[name].append(tds[-1].get_text(strip=True))
                else:
                    for key in student_scores:
                        student_scores[key].append('-')
            output_str = await _('📚 <b><i>{subj_title}</i></b>\n<i>ФИ: Курс. | Самост. | През. | Лаб. | Квиз | Мид.</i>\n', locales_dict[chat_id])
            output_str = output_str.format(subj_title=subj_title[j])
            for i, (key, value) in enumerate(student_scores.items(), start=1):
                value_sum = sum(float(x) for x in value if x != '-')
                value_str = ' | '.join(str(v) for v in value)
                line = f'{i}. {key}: <i>{value_str}</i> <b><u>{value_sum:.1f}</u></b>\n'
                output_str += line
            final_result.append(output_str) 
            j+=1
    return final_result