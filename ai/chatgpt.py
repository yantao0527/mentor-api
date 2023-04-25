# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

from app.config import Settings

settings = Settings()

openai.api_key = settings.OPENAI_API_KEY

SYSTEM_REQ="You are a helpful assistant."
USER_REQ="I provide my resume and a job description, please help me improve the resume for me."
ASSISTANT_ANS="Sure, I'd be happy to help you improve your resume. Please provide me with a copy of your resume and the job description."


def chat_improve_resume(resume, job):
    res = _improve_resume(resume, job)
    return res["choices"][0].message.content

def _improve_resume(resume, job):
    request = f"""This is my resume below

{resume}

This is a job description below

{job}

please give me an improved resume and a cover letter.
"""
    # print(request)
    # return request
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_REQ},
            {"role": "user", "content": USER_REQ},
            {"role": "assistant", "content": ASSISTANT_ANS},
            {"role": "user", "content": request}
        ]
    )
    return res
    
def _write_result(filename, res):
    new_file = open(filename,'w')
    new_file.write(res["choices"][0].message.content)
    #new_file.write(res)
    new_file.close()


if __name__ == '__main__':
    SEQ = "02"
    resume = open('ai/resume.txt','r').read()
    job = open(f"ai/job_{SEQ}.txt", 'r').read()
    
    res = chat_improve_resume(resume, job)

    _write_result(f"ai/result_{SEQ}.txt", res)
    res["choices"][0].message.content = "..."
    print(res)
