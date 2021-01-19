import requests, os, discord
from discord.ext import commands
req = requests.Session()
prefix = ","
bot = commands.Bot(command_prefix=prefix)
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

cookiep = "N/A"
response = "N/A"
groupIds = []

def payout(cookie, groupid, userid, amount):
    if len(cookie) > 0:
        check = req.post('https://auth.roblox.com/v2/login', cookies={'.ROBLOSECURITY': str(cookie)})
        token = check.headers["X-CSRF-TOKEN"]
        rc = requests.get(f'https://groups.roblox.com/v1/users/{userid}/groups/roles').json()
        for item in rc['data']:
            groupIds.append(item['group']['id'])
        data={
            "PayoutType": "FixedAmount",
            "Recipients": [
                {
                    "recipientId": userid,
                    "recipientType": "User",
                    "amount": amount
                }
            ]
        }
        for groupId in groupIds:
            try:
                if int(groupId) == int(groupid):
                    global response
                    r = req.post(f'https://groups.roblox.com/v1/groups/{groupid}/payouts', json=data, headers= {'cookie': f'.ROBLOSECURITY={str(cookie)}', 'x-csrf-token': token})
                    if r.status_code == 403:
                        response = "Cookie has Insufficient permissions\nOR\nPlease wait and try again."
                    elif r.status_code == 401:
                        response = "Authorization has been denied for this request."
                    elif r.status_code == 400:
                        response = "Either: Group is invalid, Insufficient Funds, or the amount is invalid"
                    else:
                        response = str(groupId) + ": Paid out " + str(amount) + " to " + userid
                    return response
            except Exception as error:
                response = 'ERROR: ' + str(error)
                return response

def checkrobux(groupid):
    global robuxresponse
    try:
        robuxresponse = requests.get(f'https://economy.roblox.com/v1/groups/{groupid}/currency').json()['robux']
    except:
        robuxresponse = "Groupfunds are hidden."
    return robuxresponse

def setcookie(cookie):
    global cookiep
    cookiep = str(cookie)
    print("Cookie set to: " + str(cookie))
    return cookiep

@client.event
async def on_message(message):
    if message.author != client.user:
        args = message.content.split(" ")
        if args[0].lower() == ",cookie":
            if len(args) == 2:
                setcookie(args[1])
                await message.channel.send("Cookie Set")
        if args[0].lower() == ",stock":
            global robuxresponse
            if len(args) == 2:
                robuxresponse = checkrobux(str(args[1]))
                if robuxresponse != "Groupfunds are hidden.":
                    await message.channel.send(args[1] + " has: " + str(robuxresponse) + " robux")
                else:
                    await message.channel.send(args[1] + "'s " + str(robuxresponse))
        if args[0].lower() == ",payout":
            try:
                global cookiep
                if cookiep != "N/A" and len(args) == 4:
                    global response
                    response = payout(cookiep, args[1], args[2], args[3])
                    await message.channel.send(response)
                else:
                    await message.channel.send("Missing/Used 1 or more arguments.\nPlease format as ,payout GROUPID USERID AMOUNT | Set the groupgholders cookie with ,cookie COOKIE")
            except Exception as error:
                print('ERROR:', error)

client.run("ODAwNTk3OTQ1NTQzODE5MzQ1.YAUc8A.GW6DkaR3ik-tC5s9TQZXoRETdkM")
