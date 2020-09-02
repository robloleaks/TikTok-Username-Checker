import os
import time
import requests
import threading
from urllib3 import disable_warnings
disable_warnings()


class Main:
    def __init__(self):
        self.variables = {
            'available': 0,
            'unavailable': 0,
            'retries': 0
        }

    def _checker(self, arg):
        try:
            available = requests.get(
                'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/unique/id/check/?device_id=66'
                '22992447704270341&os_version=13.6.1&residence=SE&iid=6866025950309811973&app_name='
                'musical_ly&pass-route=1&locale=sv-SE&pass-region=1&ac=WIFI&sys_region=SE&version_c'
                'ode=17.4.0&vid=09C2D5BA-EAD7-4764-9B03-A0045A96E89E&channel=App%20Store&op_region='
                'SE&os_api=18&idfa=B5AFE005-817F-4179-BCE8-11D5B64C13FA&device_platform=iphone&devi'
                'ce_type=iPhone10,5&openudid=a08e4f6286bab393c464d66e7bc51cb860c2efb8&account_regio'
                'n=&tz_name=Europe/Stockholm&tz_offset=7200&app_language=sv&carrier_region=SE&curre'
                'nt_region=SE&aid=1233&mcc_mnc=24006&screen_width=1242&uoo=0&content_language=&lang'
                'uage=sv&cdid=D3BE1FA3-8B8C-4E22-A438-7E3CE20779B0&build_number=174014&app_version='
                f'17.4.0&unique_id={arg}',
                verify=False, headers={
                    'Host': 'api16-normal-c-useast1a.tiktokv.com',
                    'Connection': 'keep-alive',
                    'x-Tt-Token': '03c3509d1a65530bf749219e146198f87432b308cd8eddff0d3f78b9a0e8de5a'
                                  '21412302d49bcb78148f1bf91fb1bb27a65',
                    'sdk-version': '1',
                    'User-Agent': 'TikTok 17.4.0 rv:174014 (iPhone; iOS 13.6.1; sv_SE) Cronet',
                    'x-tt-store-idc': 'maliva',
                    'x-tt-store-region': 'se',
                    'X-SS-DP': '1233',
                    'Accept-Encoding': 'gzip, deflate'
                }
            ).json()['is_valid']
        except Exception:
            self.variables['retries'] += 1
            self._checker(arg)
        else:
            if available:
                self.variables['available'] += 1
                print(f'[AVAILABLE] {arg}')
                with open('Available.txt', 'a') as f:
                    f.write(f'{arg}\n')
            else:
                self.variables['unavailable'] += 1
                print(f'[UNAVAILABLE] {arg}')

    def _multi_threading(self):
        threading.Thread(target=self._update_title).start()
        for username in self.usernames:
            while True:
                if threading.active_count() <= 300:
                    threading.Thread(target=self._checker, args=(username,)).start()
                    break
                else:
                    continue

    def _update_title(self):
        while (checked := (self.variables['available'] + self.variables['unavailable'])) < len(
            self.usernames
        ):
            os.system(
                f'title [TikTok Username Checker] - Checked: {checked}/{self.total_usernames} ^| Av'
                f'ailable: {self.variables["available"]} ^| Unavailable: '
                f'{self.variables["unavailable"]} ^| Retries: {self.variables["retries"]}'
            )
            time.sleep(0.2)
        os.system(
            f'title [TikTok Username Checker] - Checked: {checked}/{self.total_usernames} ^| Availa'
            f'ble: {self.variables["available"]} ^| Unavailable: {self.variables["unavailable"]} ^|'
            f' Retries: {self.variables["retries"]} && pause >NUL'
        )

    def setup(self):
        error = False
        if os.path.exists((usernames_txt := 'Usernames.txt')):
            with open(usernames_txt, 'r', encoding='UTF-8', errors='replace') as f:
                self.usernames = f.read().splitlines()
            self.total_usernames = len(self.usernames)
            if self.total_usernames == 0:
                error = True
        else:
            open(usernames_txt, 'a').close()
            error = True

        if error:
            print('[!] Paste the usernames in Usernames.txt.')
            os.system(
                'title [TikTok Username Checker] - Restart required && '
                'pause >NUL && '
                'title [TikTok Username Checker] - Exiting...'
            )
            time.sleep(3)
        else:
            self._multi_threading()


if __name__ == '__main__':
    os.system('cls && title [TikTok Username Checker]')
    main = Main()
    main.setup()
