import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from pynput.keyboard import Controller, Key


project_name = sys.argv[1]
proj_parent = os.getcwd()


# make project directory
try:
    os.mkdir(os.path.join(proj_parent, project_name))
except FileExistsError:
    copy_number = 1
    while True:
        new_name = project_name + f'_{copy_number}'
        if new_name in os.listdir(proj_parent):
            copy_number += 1
        else:
            print(
                f"[FILE EXIST ERROR]\n'{project_name}' already exists, renamed to --> '{new_name}'")
            os.mkdir(os.path.join(proj_parent, new_name))
            project_name = new_name
            break
print('[PROJECT FILE MADE]')
print(f'"{project_name}" was created in {proj_parent}')

# switch to project dir for both python script and cmd(for git commands)
os.system(f'cd {project_name}')
os.chdir(project_name)

# make readme
print('[README.md MADE]')
os.system(f"echo # {project_name} > README.md")


# make github repo
print(f'[GITHUB REPO SETUP]')
github = False
try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, port=9990)
    browser.get("https://www.github.com/login")

    user = browser.find_element_by_xpath('//*[@id="login_field"]')
    user.send_keys('hank2q')
    password = browser.find_element_by_xpath('//*[@id="password"]')
    password.send_keys(os.environ['PASSWORD'])
    browser.find_element_by_xpath(
        '//*[@id="login"]/form/div[4]/input[9]').click()  # click sign in

    # use 2 step verification with device pin
    browser.find_element_by_css_selector(
        '#login > div.auth-form-body.u2f-auth-form-body.js-u2f-auth-form-body.mt-3 > span.u2f-enabled > form > button').click()
    sleep(1)
    keyboard = Controller()
    keyboard.type('4265')

    sleep(1.7)
    browser.get("https://www.github.com/new")
    name = browser.find_element_by_xpath('//*[@id="repository_name"]')
    name.send_keys(project_name)
    sleep(1.5)
    name.send_keys(Keys.RETURN)  # create repo
    sleep(0.7)
    browser.quit()
except Exception as e:
    print('[ERROR]: couldn\'t setup gitgub repo', file=sys.stderr)
    print('The following error occured:\n', file=sys.stderr)
    print(str(e), file=sys.stderr)

else:
    github = True
    print('[GITHUB REPO MADE]')

finally:
    # initialize git in the project directory
    print('[GIT SETUP]')
    os.system('git init')
    if github:
        os.system(
            f'git remote add origin https://github.com/Hank2q/{project_name}.git')
    os.system('git add .')
    os.system('git commit -m "initial commit"')
    if github:
        os.system('git push -u origin master')
    print('[DONE]')
