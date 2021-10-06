# 한자 음가 테이블

* inspired by [suminb](https://github.com/suminb)[/hanja](https://github.com/suminb/hanja)
  * https://github.com/suminb/hanja/blob/develop/hanja/table.py
  * https://github.com/suminb/hanja/blob/develop/hanja/table.yml



###### memo

* 위 레퍼런스 코드는 한자 → 한글 변환 task에 대하여 단순 1대1 매칭 방법을 사용
  * 속도 빠름 (`yaml` dependency를 없애고 단순 Python Dictionary로 사용해도 속도 비슷)
* 문제
  * 일부 한자 누락 문제
    * 한자 목록
      * U+3400 ~ U+4DBF : [CJK Unified Ideographs Extension A](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-a/) → 수록되어 있음
      * U+4E00 ~ U+9FFF : [CJK Unified Ideographs](https://unicode-table.com/kr/blocks/cjk-unified-ideographs/)→ 수록되어 있음
      * U+F900 ~ U+FAFF : [CJK Compatibility Ideographs](https://unicode-table.com/kr/blocks/cjk-compatibility-ideographs/) → **상당수 미수록**
      * U+20000 ~ U+2A6DF : [CJK Unified Ideographs Extension B](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-b/) → **미수록**
      * U+2A700 ~ U+2B73F : [CJK Unified Ideographs Extension C](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-c/) → **미수록**
      * U+2B740 ~ U+2B81F : [CJK Unified Ideographs Extension D](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-d/) → **미수록**
      * U+2B820 ~ U+2CEAF : [CJK Unified Ideographs Extension E](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-e/) → **미수록**
      * U+2CEB0 ~ U+2EBEF : [CJK Unified Ideographs Extension F ](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-f/)→ **미수록**
      * U+2F800 ~ U+2FA1F : [CJK Compatibility Ideographs Supplement](https://unicode-table.com/kr/blocks/cjk-compatibility-ideographs-supplement/) → **미수록**
      * U+30000 ~ U+3134F : [CJK Unified Ideographs Extension G ](https://unicode-table.com/kr/blocks/cjk-unified-ideographs-extension-g/)→ **미수록**
    * *U+F900 ~ U+FAFF 사이 한자는 인터넷 상에서 대략적인 전체 음가 데이터를 구할 수 있지만,*
      *U+20000 ~ U+3134F 사이 한자는 검색하면 잘 나오지도 않음.*
  * 한국어 음가가 1개를 넘어가는 경우
    * 예시
      * [㐍](http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=14)(U+340D) : '뜰', '졸' → [suminb/hanja](https://github.com/suminb/hanja)에서는 *'졸'로만 수록*
      * [㐡](http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=34)(U+3421) : '나', '연', '유' → [suminb/hanja](https://github.com/suminb/hanja)에서는 *'유'로만 수록*
      * 樂(U+F914) : 즐거울 낙 / 樂(U+F95C) : 즐거울 락 / 樂(U+F9BF) : 좋아할 요 / [樂](http://www.koreanhistory.or.kr/newchar/list_view.jsp?code=13753)(U+6A02) : 풍류 악 → *U+F900 ~ U+FAFF 사이 (호환용) 한자의 정확한 음가 데이터 찾기 어려움 (모두 '낙', '락', '요', '악'과 매칭됨)* 
    * *새로 음가 데이터를 추가하는 한자가 2개 이상의 음가를 가지고 있는 경우, 어떤 음가 값을 수록해야할지 기준 없음*



###### 음가 데이터 출처

* ★ 한국역사정보통합시스템, [koreanhistory.or.kr](http://www.koreanhistory.or.kr/newchar/main_list.jsp)
  * Unicode Extension A 및 Unicode BMP 음가 수록
  * 일부 Unicode Extension B 수록
* ★★★ 나무위키, "[완성형/중복 한자/중복 한자 목록](https://namu.wiki/w/%EC%99%84%EC%84%B1%ED%98%95/%EC%A4%91%EB%B3%B5%20%ED%95%9C%EC%9E%90#s-5)" 문서.
  * ★★★ CJK Compatibility Ideographs 중복 음가 수록
* ★ 한국학중앙연구원 유니코드 한자 이체자 정보 사전, [waks.aks.ac.kr/unicode](http://waks.aks.ac.kr/unicode/)
  * 일부 Unicode Extension B 수록



###### reference

* [Lee, J. H.](http://doi.or.kr/10.PSN/ADPER6800413203), "[Problems with Chinese Ideographs Search in Unicode and Solutions to Them (=유니코드 한자 검색의 문제점 및 개선방안)](http://www.koreascience.or.kr/article/JAKO201220762922019.page)", 2012.07 \[[PDF](http://www.koreascience.or.kr/article/JAKO201220762922019.pdf)\]
* [unicode-table.com](https://unicode-table.com/kr/blocks/)
* Wikipedia, "[한중일 통합 한자](https://ko.wikipedia.org/wiki/%ED%95%9C%EC%A4%91%EC%9D%BC_%ED%86%B5%ED%95%A9_%ED%95%9C%EC%9E%90)" 문서.

