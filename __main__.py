import sys
import random
from lib import curio
from lib import requests
from lib.progress.spinner import Spinner
from lib.progress.spinner import PieSpinner
from lib.progress.spinner import MoonSpinner
from lib.progress.spinner import LineSpinner
from lib.progress.spinner import PixelSpinner
from lib.termcolor.termcolor import colored
from lib.colorama import just_fix_windows_console
# please don't abuse the API key, it is linked to a free account
# and can only make 20 requests per minute
api_key = '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'
spinners = [Spinner, PieSpinner, MoonSpinner, LineSpinner, PixelSpinner]

just_fix_windows_console()


def get_input(args):
	if len(args) < 2:
		raise SystemExit("You must provide an input")
	return " ".join(args[1:])


def make_request(_input):
	rsp = requests.post(
		'https://api.openai.com/v1/completions',
		json={
			"model": "text-davinci-003",
			"prompt": _input,
			"temperature": 0.5,
			"max_tokens": 2048,
		},
		headers={
			"Content-Type": "application/json",
			"Authorization": f"Bearer {api_key}"
		}
	)
	rsp.raise_for_status()
	#print(rsp.json())
	return rsp.json()['choices'][0]['text']


async def get_response(_input):
	text = await curio.run_in_thread(make_request, _input)
	print('', end='\r               \r')
	print(colored(text.lstrip(), 'light_green'))


async def spinner():
	spinner = random.choice(spinners)('Hang on ', hide_cursor=False)
	while True:
		await curio.sleep(0.2)
		spinner.next()


async def main(_input):
	async with curio.TaskGroup(wait=any) as g:
		await g.spawn(get_response(_input))
		await g.spawn(spinner)

if __name__ == '__main__':
	_input = get_input(sys.argv)
	#print(colored(_input, 'yellow'))
	curio.run(main(_input))
