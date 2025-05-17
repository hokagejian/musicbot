import asyncio
from pyrogram import Client, filters
from BrandrdXMusic import app
from BrandrdXMusic.utils.branded_ban import admin_filter

# Menyimpan task yang sedang berjalan per chat
UTAG_TASKS = {}

@app.on_message(filters.command(["utag", "uall"], prefixes=["/", "@", ".", "#"]) & admin_filter)
async def tag_all_users(_, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply_text("**Berikan teks setelah perintah, contoh:** `/utag Hai jalang!`")

    text = message.text.split(None, 1)[1]

    if chat_id in UTAG_TASKS:
        return await message.reply_text("**Proses utag sudah berjalan! Gunakan `/stoputag` untuk menghentikan.**")

    await message.reply_text(
        "**Utag dimulai!**\n➥ `sleep 7 detik`\n➥ Gunakan `/stoputag` untuk menghentikan."
    )

    async def tag_loop():
        try:
            usernum = 0
            usertxt = ""
            async for m in app.get_chat_members(chat_id):
                if chat_id not in UTAG_TASKS:
                    break
                if m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"• [{m.user.first_name}](tg://user?id={m.user.id})\n"
                if usernum == 5:
                    await app.send_message(
                        chat_id,
                        f"{text}\n\n{usertxt}\n\nGunakan /stoputag untuk menghentikan.",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(7)
                    usernum = 0
                    usertxt = ""
        except Exception as e:
            print(f"Utag error: {e}")
        finally:
            UTAG_TASKS.pop(chat_id, None)
            await app.send_message(chat_id, "**Utag selesai atau dihentikan.**")

    # Simpan task
    task = asyncio.create_task(tag_loop())
    UTAG_TASKS[chat_id] = task


@app.on_message(
    filters.command(["stoputag", "stopuall", "offutag", "offuall", "utagoff", "ualloff"], prefixes=["/", ".", "@", "#"])
    & admin_filter
)
async def stop_tagging(_, message):
    chat_id = message.chat.id
    task = UTAG_TASKS.get(chat_id)
    if task:
        task.cancel()
        UTAG_TASKS.pop(chat_id, None)
        await message.reply_text("**Berhasil menghentikan utag njing.**")
    else:
        await message.reply_text("**Tidak ada proses utag yang sedang berjalan.**")
