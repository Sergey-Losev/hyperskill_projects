from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False', echo=False)

Base = declarative_base()


class FlashCards(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)
    box = Column(Integer)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def menu_1():
    return input("""
1. Add flashcards
2. Practice flashcards
3. Exit
""")


def menu_2():
    return input("""
1. Add a new flashcard
2. Exit
""")


def menu_3():
    return input("""press "y" to see the answer:
press "n" to skip:
press "u" to update:
""")


def menu_4():
    return input("""press "d" to delete the flashcard:
press "e" to edit the flashcard:
""")


def add_flash_card():
    global session
    while True:
        choice_2 = menu_2()
        if choice_2 == "1":
            while True:
                question = input("\nQuestion:\n")
                if question.replace(" ", "") == "":
                    continue
                else:
                    while True:
                        answer = input("Answer:\n")
                        if answer.replace(" ", "") == "":
                            continue
                        else:
                            new_data = FlashCards(first_column=question, second_column=answer, box=1)
                            session.add(new_data)
                            session.commit()
                            break
                    break
        elif choice_2 == "2":
            break
        else:
            print(f"{choice_2} is not an option")


def practice():
    result_list = session.query(FlashCards).all()
    if len(result_list) == 0:
        print("There is no flashcard to practice!")
    else:
        for card in result_list:
            print(f"Question: {card.first_column}")

            choice_3 = menu_3()
            if choice_3 == 'y':
                print('Answer:', card.second_column)
                print_learn_menu(card)
            elif choice_3 == 'n':
                # print_learn_menu(card)
                continue
            elif choice_3 == 'u':
                update(card)
            else:
                print(choice_3, 'is not an option')


def update(card):
    while True:
        choice_4 = menu_4()
        if choice_4 == "e":
            print(f"current question: {card.first_column}")
            while True:
                print("please write a new question: ")
                new_quest = input()
                print()
                if new_quest == "" or new_quest == " ":
                    break
                else:
                    card.first_column = new_quest
                    session.commit()
                    print(f"current answer: {card.second_column}")
                    while True:
                        print("please write a new answer: ")
                        new_ans = input()
                        print()
                        if new_ans == "" or new_ans == " ":
                            break
                        else:
                            card.second_column = new_ans
                            session.commit()
                            break
                    break
            break
        elif choice_4 == "d":
            session.delete(card)
            session.commit()
            break
        else:
            print(choice_4, "is not an option")


def move_card_to_next_session(card):
    current_box = card.box
    card.box = current_box + 1
    session.commit()


def move_card_to_session_one(card):
    card.box == 1
    session.commit()


def delete_card(card):
    session.delete(card)
    session.commit()


def print_learn_menu(card):
    print('press "y" if your answer is correct:')
    print('press "n" if your answer is wrong:')
    a = input()
    if a == 'y':
        if card.box == 3:
            delete_card(card)
        else:
            move_card_to_next_session(card)
    elif a == 'n':
        move_card_to_session_one(card)
    else:
        print(a, 'is not an option')


def main():
    while True:
        choice_1 = menu_1()
        if choice_1 == "1":
            add_flash_card()
        elif choice_1 == "2":
            practice()
        elif choice_1 == "3":
            print('\nBye!')
            break
        else:
            print(f"{choice_1} is not an option")


if __name__ == "__main__":
    main()
