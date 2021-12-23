import requests
from bs4 import BeautifulSoup, SoupStrainer

import neckMuscle


group = neckMuscle.get_list_of_muscles_group()
neckMuscle.get_list_of_exercises(group)
