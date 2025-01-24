from PIL import Image
import discord, datetime, msg_dic, random, math, os, base64, requests, io, builtins, contextlib, sys
from time import sleep

from gradio_client import Client

msg_dict = msg_dic.msg_dic

idle = 0

from webserver import keep_alive

client = discord.Client(intents=discord.Intents.all())

# TOKEN = os.environ['TOKEN']
TOKEN = "TOKEN"


@client.event
async def on_ready():
    print("다음으로 로그인합니다: ")
    print('\"' + str(client) + '\"로 로그인 되었습니다')
    print("name: ", client.user.name)
    print("id: ", client.user.id)
    print("봇 실행 완료")
    print("----------------")
    await client.change_presence(activity=discord.Game('`제이크봇 도와줘!`라고 말해보세요!'))


@client.event
async def on_message(message):
    global idle
    msg = message.content
    if message.author == client.user:
        return
    elif msg.startswith('제이크봇'):
        if msg in msg_dict:
            await message.channel.send(
                (msg_dict[msg])[random.randint(0,
                                               len(msg_dict[msg]) - 1)])
        elif msg.startswith('제이크봇 파이썬\n'):
            python_code = "import traceback\n" + (
                "try:" + msg.split('```python')[1].split('```')[0]
            ).replace(
                "\n", "\n  "
            ) + "\nexcept Exception as e:\n  err_msg = traceback.format_exc()\n  print(str(err_msg))"
            python_input_str = None
            if len(msg.split('```python')[1].split('```')) == 3:
                try:
                    python_input_str = msg.split('```python')[1].split(
                        '```')[-2]
                    python_input_list = python_input_str.split('\n')
                except Exception:
                    pass
            await message.channel.send(
                f"Code(Python):\n```python\n{python_code}\n```")
            new_stdout = io.StringIO()
            input_func = lambda: python_input_list.pop(0)
            with contextlib.redirect_stdout(new_stdout):
                exec(python_code, {'input': input_func})
            output = new_stdout.getvalue()
            if output:
                if python_input_str not in [None, ""]:
                    await message.channel.send(
                        f"Input:\n```\n{python_input_str}\n```")
                await message.channel.send(f"Output:\n```\n{output}\n```")
        elif msg.startswith('제이크봇 아스키아트 '):
            ASCII_CHARS = [
                "@", "#", "$", "%", "?", "*", "+", ";", ":", ",", " "
            ]

            def to_greyscale(image):
                return image.convert('L')

            def pixel_to_ascii(image):
                pixels = image.getdata()
                ascii_str = ""
                for pixel in pixels:
                    ascii_str += ASCII_CHARS[pixel // 25]
                return ascii_str

            url = msg[11:]
            response = requests.get(url)
            try:
                image = Image.open(io.BytesIO(response.content))
                #image = image.resize((35, 15)) 7:5
                width, height = image.size
                image = image.resize(
                    (35, int(height / width * 35 * (5 / 7)**2)))
            except Exception:
                await message.channel.send(url + "은 잘못된 이미지 URL 입니다!")
            image = to_greyscale(image)
            ascii_str = pixel_to_ascii(image)
            img_width = image.width
            ascii_str_len = len(ascii_str)
            ascii_img = ""
            for i in range(0, ascii_str_len, img_width):
                ascii_img += ascii_str[i:i + img_width] + "\n"
            await message.channel.send("```" + ascii_img + "```")
        elif msg.startswith('제이크봇 아스키아트'):
            await message.channel.send('잘못된 이미지 URL입니다!')
        elif msg.startswith('제이크봇 base') and msg[9:11] != '':
            try:
                byte = int(msg[9:11])
                string = str.encode(msg[19:])
                if msg[12:18] == 'incode':
                    if byte == 16:
                        send = base64.b16encode(string)
                    elif byte == 32:
                        send = base64.b32encode(string)
                    elif byte == 64:
                        send = base64.b64encode(string)
                    elif byte == 85:
                        send = base64.b85encode(string)
                elif msg[12:18] == 'decode':
                    if byte == 16:
                        send = base64.b16decode(string)
                    elif byte == 32:
                        send = base64.b32decode(string)
                    elif byte == 64:
                        send = base64.b64decode(string)
                    elif byte == 85:
                        send = base64.b85decode(string)
                send = send.decode('utf-8')
                await message.channel.send(send)
            except Exception:
                await message.channel.send('오류!')
        elif msg == '제이크봇 내정보':
            user = message.author
            date = datetime.datetime.utcfromtimestamp(
                ((int(user.id) >> 22) + 1420070400000) / 1000)
            embed = discord.Embed(title=user.display_name + "님의 정보",
                                  description="사실 유저도 알 수 있는 정ㅂ...",
                                  color=0x00BBFF)
            embed.set_thumbnail(url=user.avatar)
            embed.add_field(name="가입일: ",
                            value=str(date.year) + "/" + str(date.month) +
                            "/" + str(date.day),
                            inline=True)
            embed.add_field(name="아이디: ", value=user.id, inline=True)
            embed.add_field(name="닉네임: ", value=user.name, inline=True)
            embed.set_footer(text="By i_am_jake1104")
            await message.channel.send(embed=embed)
        elif msg.startswith("제이크봇 유저정보 "):
            try:
                userid = int(message.content[9:].replace("<", "").replace(
                    ">", "").replace("@", ""))
            except Exception:
                await message.channel.send("정확히 멘션을 해주세요!")
            user = await message.guild.query_members(user_ids=[userid])
            user = user[0]
            date = datetime.datetime.utcfromtimestamp(
                ((int(user.id) >> 22) + 1420070400000) / 1000)
            embed = discord.Embed(title=user.display_name + "님의 정보",
                                  description="사실 유저도 알 수 있는 정ㅂ...",
                                  color=0x00BBFF)
            embed.set_thumbnail(url=user.avatar)
            embed.add_field(name="가입일: ",
                            value=str(date.year) + "/" + str(date.month) +
                            "/" + str(date.day),
                            inline=True)
            embed.add_field(name="아이디: ", value=user.id, inline=True)
            embed.add_field(name="닉네임: ", value=user.name, inline=True)
            embed.set_footer(text="By i_am_jake1104")
            await message.channel.send(embed=embed)
        elif msg.startswith("제이크봇 도배"):
            if message.channel.id == 998050422570889217:
                can = True
                time = msg[7:]
                try:
                    time = int(time)
                except ValueError:
                    can = False
                    if time == "":
                        await message.channel.send(
                            '도배 명령어 사용 하려면 <#998050422570889217>에서 "제이크봇 도배 [도배 횟수]" 형식으로 메시지를 보내야 합니다. 예)"제이크봇 도배 5"'
                        )
                    else:
                        await message.channel.send(
                            f'{msg[7:]}은 알맞지 않는 정수입니다.\n도배 명령어 사용 하려면 <#998050422570889217>에서 "제이크봇 도배 [도배 횟수]" 형식으로 메시지를 보내야 합니다. 예)"제이크봇 도배 5"'
                        )

                if can:
                    time = int(msg[7:])
                    formsg = ""
                    if time < 1 or time > 20:
                        await message.channel.send(
                            "도배 명령어에서 도배 횟수는 20이하인 자연수만 가능합니다")
                    else:
                        await message.channel.send(
                            f"{message.author.name}으로 인하여 <#998050422570889217>방에서 {time}번 도배\n"
                            * time)
            else:
                await message.channel.send(
                    "도배 명령어는 <#998050422570889217>에서 실행해 주세요!")
        elif msg.startswith("제이크봇 아재개그"):
            try:
                count = int(msg[10:])
                if count <= 10:
                    humor_list = msg_dic.msg_dic["제이크봇 아재개그"]
                    for i in range(count):
                        humor = humor_list[random.randint(0, len(humor_list) - 1)]
                        humor_list.remove(humor)
                        await message.channel.send(humor)
                    del humor_list
                else:
                    await message.channel.send("10초과는 불가능합니다.")
            except Exception:
                await message.channel.send("모르는 단어에요!")
        elif f"{msg.split()[0]} {msg.split()[1]}" in [
                "제이크봇 도넛", "제이크봇 Donut", "제이크봇 donut"
        ]:
            sent_msg = await message.channel.send("Donut...")
            try:
                cnt = max(0, min(int(msg.split()[-1]), 50))
            except Exception:
                cnt = 20
            donut_str = ""
            A, B = 0, 0
            while cnt > 0:  #*************#***************
                cnt -= 1
                z = [0] * 1760 #***#********************
                b = [' '] * 1760 #****************************
                for j in range(0,   628, 7):   #****************
                    for i in range(0, 628         ,2): #***********
                        c = math.sin(                 i); d = math.\
                        cos(j) ; e                       = math.sin(A)
                        f=math.sin                       ( j ) ; g = \
                        math.cos(A                       ); h = d + 2
                        D = 1 / (c                       * h * e + \
                        f *  g + 5 );                 l=math.cos(i)
                        m=math.cos(B);n =         math.sin(B)#*****
                        t= c * h * g - f * e   ; x = int ( 40 + \
                        30 * D * (l * h * m - t * n))#**********
                        __y = int(12 + 15* D * (l * h * n + t * m))
                        ____o = int(x +  80 * __y) #***************
                        ______N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
                        if 22 > __y and __y > 0 and x > 0 and 80 > x and D > z[____o]:
                            z[____o] = D; b[____o] = "0,-~:;=!*#$@"[______N if ______N > 0 else 0]
                print('\x1b[H', end='')
                for k in range(1761):
                    donut_str += b[k] if k % 80 else '\n'
                    A += 0.00004
                    B += 0.00002
                await sent_msg.edit(content="Playing Donut...\n```" +
                                    donut_str + "```")
                donut_str = ""
                sleep(0.2)
            await sent_msg.edit(content="Donut is done!")
        elif msg in ["제이크봇 꺼져", "제이크봇 ㄲㅈ"]:
            if random.randint(0, 1) == 1:
                await message.channel.send("제이크봇 전원 off(진짜로 꺼짐)")
                sys.exit()
            else:
                await message.channel.send("욕하지 마세요")
        elif msg in ['제이크봇 시계', "제이크봇 시간"]:
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            clock = await message.channel.send("{}:{}:{}".format(
                now.hour, now.minute, now.second))
            await clock.edit(
                content="{}:{}:{}".format(now.hour, now.minute, now.second))
        else:
            try:
                await message.channel.send(msg[5:] + "의 답은 " +
                                           str(eval(msg[5:])) + "입니다.")
            except Exception:
                try:
                    ai_client = Client("mangostin2010/freegpt4o")
                    result = ai_client.predict(
                        message=msg + "300자 이내로 답해줘",
                        api_name="/chat"
                    )
                    await message.channel.send(result)
                except Exception:
                    await message.channel.send("모르는 단어에요!")
    else:
        idle += random.randint(500,1200)/1000
        if 28 > idle > 27:
            idle = 0
            await message.channel.send("야!!!")
        elif 21 > idle > 20:
            await message.channel.send("나도 대화 끼어 달라고!")
            idle = 21
        elif 16 > idle > 15:
            await message.channel.send("나도 대화 끼어줘")
            idle=16


keep_alive()

client.run(TOKEN)
