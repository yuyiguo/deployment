import urllib2, urllib
try: import json
except ImportError: import simplejson as json

class Github:
  def __init__(self, token):
    self.token = token

  def GetContent(self, url, data = None, method = 'GET', headers = {}):
    headers['Authorization'] = self.token
    # See https://developer.github.com/v3/#parameters
    headers['Content-Type']  = 'application/x-www-form-urlencoded'
    headers['Accept'] = 'application/vnd.github.v3+json'
    if data: data = json.dumps(data)
    request = urllib2.Request(url, data, headers)
    request.get_method = lambda: method
    try:
      # try to open network object
      response= urllib2.urlopen(request)
    except urllib2.HTTPError, e:
      # if http error is thrown, add its status code into error
      # structure generated by github api
      ret = json.loads(e.read())
      ret['HTTPStatusCode'] = e.code
      return ret
    return json.loads(response.read())

  def GetRateLimit(self):
    return self.GetContent('https://api.github.com/rate_limit')

  def GetPullRequests(self, owner, repo):
    return self.GetContent('https://api.github.com/repos/%s/%s/pulls' % (owner, repo))

  def MergePullRequest(self, pullRequest, msg):
    url  = pullRequest['url'] + '/merge'
    data = {'commit_message' : msg}
    return self.GetContent(url, data, method = 'PUT')

  def GetComments(self, comments_url):
    return self.GetContent(comments_url)

  def Comment2PullRequest(self, pullRequest,  msg):
    url  = pullRequest['comments_url']
    data = {'body':msg}
    return self.GetContent(url, data, method = 'POST')

  def GetStatus(self, status_url):
    return self.GetContent(status_url)

  def PostStatus(self, status_url, state='success', msg="Continuous integration from CMS COMP build-agent."):
    data = {'state': state,
            'description': msg
           }
            #'target_url': 'http://cern.ch/cms-dmwm-builds',
            #'context': 'continuous-integration/cms-comp-build-agent'
    return self.GetContent(status_url, data, method = 'POST')

  def GetBranches(self, owner, repo):
    return self.GetContent('https://api.github.com/repos/%s/%s/branches' % (owner, repo))

  def GetTags(self, owner, repo):
    return self.GetContent('https://api.github.com/repos/%s/%s/tags' % (owner, repo))

  def GetLatestCommit(self, owner, repo, branch):
    return self.GetContent('https://api.github.com/repos/%s/%s/commits/%s' % (owner, repo, branch))
