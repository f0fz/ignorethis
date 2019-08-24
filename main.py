#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

from functions.init import TYPING_NRIC, ENDSEM, QN2, QN3, ENDPOST, ADMIN_START, ADMIN_END, NEW_ADMIN
from functions import seminar, post_seminar, utils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("241346491:AAH09_cf9KfaFohGgXUo96ljvOeyqcD1k4o")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states TYPING_NRIC and RESPONSE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', seminar.start)],
        states={
            TYPING_NRIC: [MessageHandler(Filters.text,
                                         seminar.get_nric,
                                         pass_user_data=True)],
            ENDSEM: [RegexHandler('^Yes|No$',
                                  seminar.final,
                                  pass_user_data=True)]
        },
        fallbacks=[]
    )

    # Add conversation handler with the states QN1, QN2, QN3
    post_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('postevent', post_seminar.postevent)],
        states={
            QN2: [MessageHandler(Filters.text,
                                 post_seminar.question2,
                                 pass_user_data=True)],
            QN3: [MessageHandler(Filters.text,
                                 post_seminar.question3,
                                 pass_user_data=True)],
            ENDPOST: [MessageHandler(Filters.text,
                                     post_seminar.endPost,
                                     pass_user_data=True)]
        },
        fallbacks=[]
    )

    # Add conversation handler with the states ADMIN_START, ADMIN_END
    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('changeText', utils.startChangeChat, pass_user_data=True, pass_args=True)],
        states={
            ADMIN_START: [MessageHandler(Filters.text,
                                         utils.receiveChatToChange,
                                         pass_user_data=True)],
            ADMIN_END: [MessageHandler(Filters.text,
                                       utils.updateChatText,
                                       pass_user_data=True)]
        },
        fallbacks=[]
    )

    # Add conversation handler with the state NEW_ADMIN_END
    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('newAdmin', utils.startNewAdmin)],
        states={
            NEW_ADMIN: [MessageHandler(Filters.contact,
                                       utils.addNewAdmin)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(post_conv_handler)
    dp.add_handler(admin_handler)
    dp.add_handler(CommandHandler('help', utils.adminHelp))
    dp.add_handler(CommandHandler('id', utils.chatID))
    dp.add_handler(CommandHandler('aStats', utils.attendanceStats))
    dp.add_handler(CommandHandler('fStats', utils.feedbackStats))
    dp.add_handler(CommandHandler('aFile', utils.sendAttendanceFile))
    dp.add_handler(CommandHandler('fFile', utils.sendFeedbackFile))
    dp.add_handler(CommandHandler('listAdmins', utils.listAllAdmins))
    dp.add_handler(CommandHandler('removeAdmin', utils.listAllAdmins, pass_args=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info("The bot is running.")
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
