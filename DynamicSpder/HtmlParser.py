import re
import json
import codecs

class HtmlParser(object):

    def url_parser(self, url, response):
        p = re.compile(r'(http://movie.mtime.com/(\d+)/)')
        urls = p.findall(response)
        if urls != None:
            return list(set(urls))
        else:
            return None

    def json_parser(self, url, response):
        p = re.compile(r'=(.+?);')
        result = p.findall(response)[0]
        if result != None:
            value = json.loads(result)
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception as e:
                print(e)
                return None
            if isRelease:
                if value.get('value').get('hotValue') == None:
                    return self._parser_release(url, value)
                else:
                    return self._parser_no_release(url, value, isRelease=2)
            else:
                return self._parser_no_release(url, value)


    def _parser_release(self, url, value):
        try:
            isRelease = 1
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')
            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')
            ShowDays = boxOffice.get('ShowDays')
            try:
                Rank = boxOffice.get('Rank')
            except Exception as e:
                Rank = 0
            return (MovieId, movieTitle, RatingFinal, ROtherFinal, RPictureFinal, RDirectorFinal,
                    RStoryFinal, Usercount, AttitudeCount,str(TotalBoxOffice+TotalBoxOfficeUnit),
                    str(TodayBoxOffice+TodayBoxOfficeUnit), Rank, ShowDays, isRelease)
        except Exception as e:
            print(e, url, value)
            return None

    def _parser_no_release(self,url,value,isRelease=0):
        try:
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')
            RDirectorFinal = movieRating.get('RDirectorFinal')
            ROtherFinal = movieRating.get('ROtherFinal')
            RatingFinal = movieRating.get('RatingFinal')
            MovieId = movieRating.get('MovieId')
            Usercount = movieRating.get('Usercount')
            AttitudeCount = movieRating.get('AttitudeCount')
            try:
                Rank = value.get('value').get('hotValue').get('Ranking')
            except Exception as e:
                Rank = 0
            return (MovieId, movieTitle, RatingFinal, ROtherFinal, RPictureFinal, RDirectorFinal,
                    RStoryFinal, Usercount, AttitudeCount, '无','无', Rank, 0, isRelease)
        except Exception as e:
            print(e, url, value)
            return None

