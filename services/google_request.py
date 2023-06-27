import requests
from bs4 import BeautifulSoup

class GoogleRequest:
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Accept-Language': 'ru-RU, ru;q=0.9, en-US;q=0.8, en;q=0.7, fr;q=0.6'
  }

  def find(self, phrase):
    req = phrase.replace(' ', '+')
    res = ''
    google_req = f'https://www.google.com/search?sxsrf=ALeKk01ZA2k6IK85yDRhcN2Ovn-yI3_SJg%3A1588929244654&ei=3CK1Xpe3J7GLmwW4_pDoBA&q={req}+это&oq={req}+это&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46BAgAEEc6BAgjECc6BQgAEIMBOgcIABCDARBDOgQIABBDOgcIIxDqAhAnUNK-AVjT6QFggOwBaAJwAXgAgAGiAYgBhRCSAQQwLjE2mAEAoAEBqgEHZ3dzLXdperABCg&sclient=psy-ab&ved=0ahUKEwiXlc3Z9qPpAhWxxaYKHTg_BE0Q4dUDCAw&uact=5'

    try:
      full_page = requests.get(google_req, headers=self.headers)
      soup = BeautifulSoup(full_page.content, 'html.parser')

      convert: BeautifulSoup = soup.findAll('div', {'jscontroller': 'GCSbhd', 'class': 'kno-rdesc', 'jsaction': 'seM7Qe:c0XUbe;Iigoee:c0XUbe;rcuQ6b:npT2md'})
      span_elements = convert[0].find_all('span')

      if len(span_elements) > 3:
        res = span_elements[2].text
      elif len(span_elements):
        res = span_elements[0].text
    except:
      print('Google response error.')

    return res

google_request = GoogleRequest()
