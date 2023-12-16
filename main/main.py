# Importing libs
from telethon.sync import TelegramClient, events

# Remplacez 'api_id', 'api_hash', 'phone_number' par vos propres valeurs
api_id = 0  # Api hash ID in https://my.telegram.org/apps
api_hash = ''  # Your api hash created on https://my.telegram.org/apps
phone_number = ''  # your phone number

groups = [-5133725807]  # the groups to spy messages

forwarding_group = -5133725807  # the group to forward messages


def saveMessage(message: str):  # function for save message on the txt file
    f = open("./output/output.txt", "a", encoding="Utf-8")  # opening the file
    f.write(message + "\n")  # write the lines
    f.close()  # close the file


if not api_id or not api_hash or not phone_number:  # some verifications
    print(
        "Please provide Api_ID : int and api_hash : string and your phone number in phone_number\nThey are provided on https://my.telegram.org/apps")

else:

    with TelegramClient('session_name', api_id, api_hash) as client:
        client.connect()  # connect Client

        if not client.is_user_authorized():  # if the client isn't verified
            client.send_code_request(phone_number)  # get code request
            client.sign_in(phone_number, input('Enter the code: '))  # Enter received verification code


        @client.on(events.NewMessage(chats=groups))
        async def message_handler(event):  # event listener for messages in specific groups
            sender = await event.get_sender()  # getting the sender of the message
            print(f"Message received in channel/group {event.chat.title}:")

            message = f"[{event.chat.title}][{event.chat.id}][{event.message.date}] - [{sender.first_name} {sender.last_name}] {event.message.message}"
            print(message)

            saveMessage(message)  # saving message in the txt file

            await client.send_message(forwarding_group, message)  # sending the message on the forwarding group

            print(f"Message successfully send in the {forwarding_group}")


        print("Waiting for new messages in the specified channels/group...")
        client.run_until_disconnected()  # running client
