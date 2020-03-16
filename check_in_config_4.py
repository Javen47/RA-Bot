# Which check-in are these questions for?
CHECK_IN_NUMBER = 4

# The message that will be displayed before the questions are asked.
CHECK_IN_HEADER_MESSAGE = '\nHello, thank you for taking the time with this check-in!\nThe following questions are ' \
                          'not a quiz, ' \
                          'more so a guideline for you to let me know how you are doing. Feel free to talk about' \
                          ' whatever is on your mind. \n-' \
                          '\nYou can respond using separate messages. ' \
                          'Please give context to your answers with respect to each question.\n '

# Redundant check-in questions
CHECK_IN_QUESTIONS_SAME = ['How are you processing all the recent dramatic changes?',
                           'On a 1-10 scale (10 being overwhelmed), how would you rank your stress levels?',
                           'With so much happening, how are you doing with self-care and your routine? Have '
                           'you explored how things might change?',
                           'How have you adjusted your academic routine?',
                           'What are you going to do if your routine isn’t working? '
                           'What are you doing to take care of yourself mentally and emotionally?',
                           'What has your support system looked like as of recent?',
                           'How is your current living situation?',
                           'Is there anything I can do to help you while you’re away?']

# Check-in questions for returning students.
CHECK_IN_QUESTIONS_FIRST_YEARS = CHECK_IN_QUESTIONS_SAME

# Check-in questions for first year students.
CHECK_IN_QUESTIONS_RETURNERS = CHECK_IN_QUESTIONS_SAME
