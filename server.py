# This file provided by Facebook is for non-commercial testing and evaluation
# purposes only. Facebook reserves all rights not expressly granted.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
import time
from flask import Flask, Response, request
import pusher

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

pusher = pusher.Pusher(
  app_id='196661',
  key='f829ca5282dc97707d03',
  secret='147b477572416cbd712f'
)
@app.route('/api/comments', methods=['GET', 'POST'])
def new_message():

	with open('comments.json', 'r') as file:
		comments = json.loads(file.read())
		
	if request.method == 'POST':
		newComment = request.form.to_dict()
		newComment['author']=newComment['author'][:16]
		newComment['text']=newComment['text'][:200]
		newComment['id'] = str(int(time.time() * 1000))
		comments.append(newComment)

		with open('comments.json', 'w') as file:
			file.write(json.dumps(comments, indent=4, separators=(',', ': ')))
			
		pusher.trigger('messages', 'new_message', {
			"author":newComment['author'],
			"text":newComment['text'],
			"id":newComment['id']
		})

	return Response(json.dumps(comments), mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

	
if __name__ == '__main__':
    app.run(host= '10.1.1.100',port=int(os.environ.get("PORT",3000)))