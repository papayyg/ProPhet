import asyncio
import aiohttp

current_sem = 1


async def try_auth(login, password):
    async with aiohttp.ClientSession() as session:
        json_data = {
            'username': login,
            'password': password,
        }
        response = await session.post("https://empro.naa.edu.az/AuthRest/login", json=json_data)
        if "Auth" in response.headers: return True
        else: return False
        
async def get_auth(login, password, session):
    json_data = {
        'username': login,
        'password': password,
    }
    answer = await session.post("https://empro.naa.edu.az/AuthRest/login", json=json_data)
    answer_json = await answer.json()
    name = f'{answer_json["data"]["firstname"]} {answer_json["data"]["lastname"]}'

    headers = {
        'Auth': f'Education {answer.headers["Auth"]}'
    }
    return headers, name


async def get_nb(login, password):
    async with aiohttp.ClientSession() as session:
        headers, name = await get_auth(login, password, session)
        data = '{"kv":{"lang":"az"}}'
        answer = await session.post("https://empro.naa.edu.az/AuthRest/api/jwt/EducationSystem/EduYear/GetEduYearByCommon", headers=headers, data=data)
        answer_json = await answer.json()
        year_id = answer_json['tbl'][0]['r'][0]['id']

        data = '{"kv":{"typeId":"100000048","lang":"az"}}'
        answer = await session.post('https://empro.naa.edu.az/AuthRest/api/jwt/EducationSystem/Dictionaries/GetDictionariesListByCommon', headers=headers, data=data)
        answer_json = await answer.json()
        sem_id = answer_json['tbl'][0]['r'][current_sem]['id']

        json_data = {
            'kv': {
                'eduYearId': year_id,
                'semesterId': sem_id,
                'lang': 'az',
            },
        }
        answer = await session.post('https://empro.naa.edu.az/AuthRest/api/jwt/EducationSystem/Report/GetStudentCourseQbLimitReport', headers=headers, json=json_data)
        answer_json = await answer.json()
        output_message = f'<b>{name.title()}</b>\n'
        for item in answer_json['tbl'][0]['r']:
            qb_count = int(item['qbCount'])
            qb_limit = int(item['qbKesr']) - 1
            if qb_count < qb_limit*20/100:
                smile = '🔵'
            elif qb_count < qb_limit*40/100:
                smile = '🟢'
            elif qb_count < qb_limit*60/100:
                smile = '🟡'
            elif qb_count < qb_limit*80/100:
                smile = '🟠'
            elif qb_count <= qb_limit:
                smile = '🔴'
            elif qb_count > qb_limit:
                smile = '❌'
            else:
                smile = '⚪️'
            one_point = item['qbForPoint1']
            two_point = item['qbForPoint2']
            subj_name = item['subjectName'][:20] if len(
                item['subjectName']) >= 20 else item['subjectName']
            row = f'{smile} <b>{qb_count}/{qb_limit}</b> {subj_name}: (<b>{one_point}, {two_point}</b>)\n'
            output_message += row
        return output_message


async def get_journal(login, password, chat_id):
    async with aiohttp.ClientSession() as session:
        headers, name = await get_auth(login, password, session)
        output_list = []
        json_data = {
            'kv': {
                'typeCode': 'CURRENT',
                'currentStatus': 'CURRENT',
                'lang': 'az',
            },
        }
        answer = await session.post('https://empro.naa.edu.az/AuthRest/api/jwt/EducationSystem/CourseView/GetStudentTranscript', headers=headers, json=json_data)
        answer_json = await answer.json()
        for item in answer_json['tbl'][0]['r']:
            subj_id = item['courseId']
            subj_title = item['subjectName']

            json_data = {
                'kv': {
                    'courseId': subj_id,
                    'currentStatus': 'CURRENT',
                    'lang': 'az',
                },
            }
            answer = await session.post('https://empro.naa.edu.az/AuthRest/api/jwt/EducationSystem/CourseView/GetReportCourseOverview', headers=headers, json=json_data)
            answer_json = await answer.json()
            output_str = f'👤 <b>{name.title()}</b>\n\n📚 <b>{subj_title}</b>\n'
            for point in answer_json['tbl'][0]['r']:
                if point['evaluationName'] == 'Kurs işi':
                    output_str += f'Курсовая работа: <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i>\n'
                elif point['evaluationName'] == "Imtahana qeder bal":
                    pre_exam = f'Балл до экзамена: <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i>\n'
                elif point['evaluationName'] == "Yekun bal":
                    full = f'Итоговый балл (Буква): <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i> ({answer_json["kv"]["pointWord"]})\n'
                elif point['evaluationName'] == "Davamiyyət":
                    qb = f'Посещаемость: <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i>\n'
                elif point['evaluationName'] == "İmtahan":
                    exam = f'Экзамен: <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i>\n'
                elif point['evaluationName'] == "Dəsr aktivliyi":
                    json_data = {
                        'kv': {
                            'startLimit': 1,
                            'endLimit': 7,
                            'courseId': subj_id,
                            'currentStatus': 'CURRENT',
                            'lang': 'az',
                        },
                    }
                    cl = await session.post('https://empro.naa.edu.az/AuthRest/api/jwt/EducationSystem/CourseView/GetInColloquiumStudentPointList', headers=headers, json=json_data)
                    cl_json = await cl.json()
                    if len(cl_json["tbl"]) > 0:
                        colloquium = float(cl_json["tbl"][0]["r"][0]["point"])
                    else: colloquium = 0
                    active = float(point["averagePoint"]) - colloquium
                    full_active = f'\nКоллоквиум: {colloquium}\nАктивность без коллоквиума: {active}\nИтоговая активность: <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i>\n\n'
                elif point['evaluationName'] == "Sərbəst iş":
                    work = f'Самостоятельная работа: <i>{point["averagePoint"]}/{point["evaMaxPoint"]}</i>\n'
                
            output_str = output_str + qb + work + full_active + pre_exam + exam + full
            output_list.append(output_str)
    return output_list