import time
from DynamicSpder.HtmlDownloader import HtmlDownloader
from DynamicSpder.HtmlParser import HtmlParser
from DynamicSpder.DataOutput import DataOutput


class Spider(object):


    def __init__(self):
        self.download = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,root_url):
        content = self.download.download(root_url)
        urls = self.parser.url_parser(root_url, content)
        for url in urls:

            t = time.strftime('%Y%m%d%H%M%S3282', time.localtime())
            rank_url = 'http://service.library.mtime.com/Movie.api' \
                       '?Ajax_CallBack=true' \
                       '&Ajax_CallBackType=Mtime.Library.Services' \
                       '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                       '&Ajax_CrossDomain=1' \
                       '&Ajax_RequestUrl=%s' \
                       '&t=%s' \
                       '&Ajax_CallBackArgument0=%s'%(url[0],t,url[1])
            rank_content = self.download.download(rank_url)
            data = self.parser.json_parser(rank_url,rank_content)
            self.output.store_data(data)

        self.output.output_end()
        print('crawl finished')


if __name__ == '__main__':
    Spider().crawl('http://theater.mtime.com/China_Jiangsu_Province_Nanjing/')