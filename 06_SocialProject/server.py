import asyncio
import cowsay


clients = {}
login2client = {}

available_cows = cowsay.list_cows()

async def chat(reader, writer):
    is_registered = False
    my_login = ""
    is_quit = False
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof() and not is_quit:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                query = q.result().decode().strip()

                if not query:
                    break

                parsed_query = query.split()
                command = parsed_query[0]

                if command == "cows":
                    ans = "Available cows:\n" + "".join(list(map(lambda x: " " + "*" + " " + x + "\n", available_cows)))
                    writer.write(ans.encode())
                    await writer.drain()
                elif command == "login":
                    cow_name = parsed_query[1]
                    if cow_name not in available_cows:
                        ans = "This cow name is not available! Try another name\n"
                        writer.write(ans.encode())
                        await writer.drain()
                    else:
                        is_registered = True
                        my_login = cow_name
                        available_cows.remove(cow_name)
                        login2client[cow_name] = me
                        ans = "You have successfully registered!\n";
                        writer.write(ans.encode())
                        await writer.drain()
                elif command == "who":
                    if not is_registered:
                        ans = "You are not registered!\n";
                        writer.write(ans.encode())
                        await writer.drain()
                        continue
                    ans = "Registered users:\n" + "".join(list(map(lambda x: " " + "*" + " " + x + "\n", list(login2client.keys()))))
                    writer.write(ans.encode())
                    await writer.drain()
                elif command == "say":
                    if not is_registered:
                        ans = "You are not registered!\n";
                        writer.write(ans.encode())
                        await writer.drain()
                        continue

                    other_user = parsed_query[1]
                    if other_user == my_login:
                        ans = "You can't send messages to yourself!\n"
                        writer.write(ans.encode())
                        await writer.drain()
                        continue
                    elif other_user not in login2client:
                        ans = f"There is no registered user with the username: {other_user}\n"
                        writer.write(ans.encode())
                        await writer.drain()
                        continue

                    message = f"Message from user: {my_login}\n" + cowsay.cowsay(cow=my_login, message=" ".join(parsed_query[2:]))
                    
                    other_client_id = login2client[other_user]
                    await clients[other_client_id].put(message)

                elif command == "yield":
                    if not is_registered:
                        ans = "You are not registered!\n";
                        writer.write(ans.encode())
                        await writer.drain()
                        continue

                    message = f"Message from user: {my_login}\n" + cowsay.cowsay(cow=my_login, message=" ".join(parsed_query[1:]))
                    for client in login2client.values():
                        out = clients[client]
                        if out is not clients[me]:
                            await out.put(message)

                elif command == "quit":
                    is_quit = True
                    break

                elif command == "completelogin":
                    ans = "completelogin " + " ".join(available_cows)
                    writer.write(ans.encode())
                    await writer.drain()
                elif command == "completesay":
                    ans = "completesay " + " ".join(list(login2client.keys()))
                    writer.write(ans.encode())
                    await writer.drain()
                else:
                    ans = "You entered the wrong command!\n";
                    writer.write(ans.encode())
                    await writer.drain()

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    available_cows.append(my_login)
    if my_login in login2client:
        del login2client[my_login]
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
