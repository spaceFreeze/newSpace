var list1;
var list2;
var list3;

var totalData = 0;    // 총 데이터 수
var currentPage = 1;  // 현재 페이지 수
var dataPerPage = 8;  // 한 페이지에 나타낼 데이터 수
var pageCount = 5;    // 한 화면에 나타낼 페이지 수
var totalPage = 0;    // 총 페이지 수
var pageGroup = 0;    // 페이지 그룹

var gType;
var gMenuName;

function menuEvent(element, type, currentPage){
  var baseUrl = 'http://127.0.0.1:5000/'; 
  var menuName = $(element).children('p').text();
  gType = type;
  gMenuName = decodeURI(decodeURIComponent(menuName));
  var menuId = $(element).attr('id');

  if (currentPage == undefined) currentPage = '1';

  if(type == 'idm'){
    $("#sections ul li").children('.active').attr('class', 'nav-link');
    $("#idm ul li").children('.active').attr('class', 'nav-link');
    $("#fabless ul li").children('.active').attr('class', 'nav-link');
    $("#foundry ul li").children('.active').attr('class', 'nav-link');
    $("#enterprisesTitle").attr('class', 'nav-link active');
    $("#sectionsTitle").attr('class', 'nav-link');
    $(element).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');

    menuUrl = 'all' + '/' + gMenuName + '/' + currentPage;
  }else if (type == 'fabless'){
    $("#sections ul li").children('.active').attr('class', 'nav-link');
    $("#idm ul li").children('.active').attr('class', 'nav-link');
    $("#fabless ul li").children('.active').attr('class', 'nav-link');
    $("#foundry ul li").children('.active').attr('class', 'nav-link');
    $("#enterprisesTitle").attr('class', 'nav-link active');
    $("#sectionsTitle").attr('class', 'nav-link');
    $(element).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');

    menuUrl = 'all' + '/' + gMenuName + '/' + currentPage;
  }else if (type == 'foundry'){
    $("#sections ul li").children('.active').attr('class', 'nav-link');
    $("#idm ul li").children('.active').attr('class', 'nav-link');
    $("#fabless ul li").children('.active').attr('class', 'nav-link');
    $("#foundry ul li").children('.active').attr('class', 'nav-link');
    $("#enterprisesTitle").attr('class', 'nav-link active');
    $("#sectionsTitle").attr('class', 'nav-link');
    $(element).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');

    menuUrl = 'all' + '/' + gMenuName + '/' + currentPage;
  }else{
    $("#sections ul li").children('.active').attr('class', 'nav-link');
    $("#idm ul li").children('.active').attr('class', 'nav-link');
    $("#fabless ul li").children('.active').attr('class', 'nav-link');
    $("#foundry ul li").children('.active').attr('class', 'nav-link');
    $("#sectionsTitle").attr('class', 'nav-link active');
    $("#enterprisesTitle").attr('class', 'nav-link');
    $(element).attr('class', 'nav-link active');
    $('#directName').text('Sections');

    menuUrl = gMenuName + '/' + 'all' + '/' + currentPage;
  }
    
  //var baseUrl = 'http://127.0.0.1:5000/main/1'; 
  //url = baseUrl + 'dist/json.json'; 
  //IT/all/1
  var url = baseUrl + menuUrl;

  // getUrl(url, type, menuName);
  document.location.href='index.html?type=' + gType + '&menuId=' + menuId + '&menuName=' + encodeURI(encodeURIComponent(gMenuName));
}

function getUrl(url, type, menuName, menuId) {

  if(type == undefined) gType = 'all';
  if(menuName == undefined) gMenuName = 'all';

  loadItems(url).then((items) => {
    itemsStr = JSON.stringify(items); 
    itemsStr = JSON.parse(itemsStr); 

    totalData = itemsStr.list1.total;
    currentPage = itemsStr.list1.page;

    list1 = itemsStr.list1.list;

    newsList1(list1, type, menuName, menuId);
    paging(totalData, dataPerPage, pageCount, currentPage, menuId);
  })
  .catch(function(error) {
    console.log('There has been a problem with your fetch operation: ', error.message);
    $('#newsList1').html('');
    $('#paging').html('');
  });
}

function loadItems(url) {
    return fetch(url)
        .then((response) => response.json()) 
        .then((json) => json); 
}
		
function paging(totalData, dataPerPage, pageCount, currentPage, menuId) {

  totalPage = Math.ceil(totalData / dataPerPage);    // 총 페이지 수
  pageGroup = Math.ceil(currentPage / pageCount);    // 페이지 그룹

  if (totalPage < pageCount) pageCount = totalPage;

  console.log("====================");
  console.log("totalData:", totalData)
  console.log("totalPage :",  totalPage);  // 총 페이지 수
  console.log("pageGroup :", pageGroup);  // 현재 페이지 그룹
  console.log("currentPage :", currentPage);  // 현재 페이지 수

  var last = pageGroup * pageCount;    // 마지막 페이지 번호  // pageCount: 5
  if (last > totalPage)  // 마지막 그룹의 페이지 수가 다 못 채워질 경우(ex. 총 12페이지)
    last = totalPage;    // 마지막 페이지 번호 = 12

  var next = parseInt(currentPage) + 1; // 덧셈 연산 시 문자열로 변환된 후 실행되는 듯
  var prev = currentPage - 1;
  var first = last - (pageCount - 1);    // 첫 번째 페이지 번호

  var fnext = last + 1;  // 다음 페이지 그룹의 첫 번째 페이지 번호
  var fprev = first - 1; // 다음 페이지 그룹의 마지막 페이지 번호

  console.log("====================");
  console.log("last : " + last);   // 마지막 페이지 번호
  console.log("first : " + first); // 첫 번째 페이지 번호
  console.log("next : " + next);   // 현재 페이지 + 1
  console.log("prev : " + prev);   // 현재 페이지 - 1
  console.log("fnext : " + fnext); // 다음 페이지 그룹의 첫 번째 페이지 번호
  console.log("fprev : " + fprev); // 다음 페이지 그룹의 마지막 페이지 번호
  console.log("====================");

  var $pingingView = $("#paging");

  var html = "";

  // 2번째 pageGroup부터 << 표시
  if (pageGroup > 1)
    html += "<a href=# menuId=" + menuId + " id='fprev' style=\"margin:20px;\"><<</a>";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  // 2페이지부터 < 표시
  if (prev > 0)
    html += "<a href=# menuId=" + menuId + " id='prev' style=\"margin:20px;\"><</a> ";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  // 페이지 번호
  for (var i = first; i <= last; i++) {
    html += "<a href=# menuId=" + menuId + " id=" + i + " style=\"display:inline-block; margin:20px;\">" + i + "</a> ";
  }

  // 다음 페이지가 존재할 때 > 표시
  if (next <= totalPage)
    html += "<a href=# menuId=" + menuId + " id='next' style=\"margin:20px;\">></a>";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  // 마지막 pageGroup을 제외하고 >> 표시
  if (last < totalPage) 
    html += "<a href=# menuId=" + menuId + " id='fnext' style=\"margin:20px;\">>></a>";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  // 페이지 목록 생성
  $("#paging").html(html);    
  $("#paging a").css({
    "color": "#A6A6A6",
    "font-size": "20"
  });
  $("#paging a#" + currentPage).css({  // 현재 페이지 표시
    "text-decoration": "none",
    "color": "#007BFF",
    "font-size": "20",
    "font-weight": "bold"
  });    
  console.log("html : " + html);
}

function newsList1(list, type, menuName, menuId) {
    var genHtml = '';
    list.forEach(function(json, idx){
        console.log(idx);

        fiusrc = '';
        if (json.img_url == 'none') {
            fiusrc = 'dist/img/noimg3.png';
        } else {
            fiusrc = json.img_url;
        }

        genHtml += '<!-- col -->';
        genHtml += '<div class="col-12">';
        genHtml += '  <!-- Default box -->';
        genHtml += '  <div class="card">';
        genHtml += '    <div class="card-header">';
        genHtml += '      <h3 class="card-title"><font size="3em"><strong>' + json.title + '&nbsp;&nbsp;<a href="' + json.url + '" target="_blank"><strong><i class="far fa-file-alt mr-1"></i></strong></a></strong></font></h3>';

        genHtml += '      <div class="card-tools">';
        genHtml += '        <button type="button" class="btn btn-tool" data-card-widget="collapse" title="Collapse">';
        genHtml += '          <i class="fas fa-minus"></i>';
        genHtml += '        </button>';
        genHtml += '        <button type="button" class="btn btn-tool" data-card-widget="remove" title="Remove">';
        genHtml += '          <i class="fas fa-times"></i>';
        genHtml += '        </button>';
        genHtml += '      </div>';
        genHtml += '    </div>';
        genHtml += '    <div class="card-body">';
        genHtml += '      <!-- post text -->';
        genHtml += '      <img class="attachment-img" src="' + fiusrc + '" alt="News Image" width="180" height="180" id="#hp" align="right" style="border-radius: 7px;">';
        
        genHtml += '      <p>' + json.summaries + '</p>';
        
        genHtml += '    </div>';
        genHtml += '    <!-- /.card-body -->';
        
        genHtml += '    <div class="card-footer">';

        (json.hashtag).forEach(function(data, idx){
          genHtml += '		<button type="button" class="btn btn-default btn-sm" onclick=window.open("keyword.html?type=' + gType + '&menuId=' + menuId + '&menuName=' + encodeURI(gMenuName) + '&keyword=' + encodeURI(encodeURIComponent(data['hash'+(idx+1)])) + '","_top")>' + '#' + data['hash'+(idx+1)] + '</button>';
        });

        genHtml += '    </div>';
        genHtml += '    <!-- /.card-footer-->';
        genHtml += '  </div>';
        genHtml += '  <!-- /.card -->';
        genHtml += '</div>';
        genHtml += '<!-- /.col -->';
    });
    
    $('#newsList1').html(genHtml);
    //copy();
}

function Request(){
  var requestParam ="";
  
  //getParameter Function
   this.getParameter = function(param){
   //현재 주소를 decoding
   var url = unescape(location.href);
   //파라미터만 자르고, 다시 &구분자를 잘라서 배열에 넣는다.
    var paramArr = (url.substring(url.indexOf("?")+1,url.length)).split("&");
  
    for(var i = 0 ; i < paramArr.length ; i++){
      var temp = paramArr[i].split("="); //파라미터 변수명을 담음
  
      if(temp[0].toUpperCase() == param.toUpperCase()){
        // 변수명과 일치할 경우 데이터 삽입
        requestParam = paramArr[i].split("=")[1];
        break;
      }
    }
    return requestParam;
  }
}
 
$(document).ready(function() {

  // Request 객체 생성
  var request = new Request();

  var keyword = request.getParameter("keyword");
  var type = request.getParameter("type");
  var menuId = request.getParameter("menuId");
  gType = type;
  var menuName = request.getParameter("menuName");
  gMenuName = menuName;

  console.log('keyword : '+ decodeURI(decodeURIComponent(keyword)));
  console.log('type : '+ type);
  console.log('menuName : '+ decodeURI(decodeURIComponent(menuName)));

  var baseUrl = 'http://127.0.0.1:5000/hash';

  var url = '';
  if (type == 'sections') {
    url = baseUrl + '/' + gMenuName + '/' + 'all' + '/' + keyword + '/' + currentPage;
  } else if (type == 'idm') {
    url = baseUrl + '/' + 'all' + '/' + gMenuName + '/' + keyword + '/' + currentPage;
  } else if (type == 'fabless') {
    url = baseUrl + '/' + 'all' + '/' + gMenuName + '/' + keyword + '/' + currentPage;
  } else if (type == 'foundry') {
    url = baseUrl + '/' + 'all' + '/' + gMenuName + '/' + keyword + '/' + currentPage;
  } else {
    url = baseUrl + '/' + 'all' + '/' + 'all' + '/' + keyword + '/' + currentPage;
  }

  $('#keywordName').text('#' + decodeURI(decodeURIComponent(keyword))); 
  
 // http://127.0.0.1:5000/hash/IT/all/중국/1
 // http://127.0.0.1:5000/hash/all/삼성전자/중국/1
 // http://127.0.0.1:5000/hash/all/삼성전자/중국/1

  console.log('keyword url : ' + url);

  getUrl(url, gType, gMenuName, menuId);

  if(gType == 'idm'){
		$("#sections ul li").children('.active').attr('class', 'nav-link');
		$("#idm ul li").children('.active').attr('class', 'nav-link');
		$("#fabless ul li").children('.active').attr('class', 'nav-link');
		$("#foundry ul li").children('.active').attr('class', 'nav-link');
		$("#enterprisesTitle").attr('class', 'nav-link active');
		$("#sectionsTitle").attr('class', 'nav-link');
    $('#idm ul').attr('style', '');
    $('#idm').attr('class', 'nav-item menu-is-opening menu-open');
      $('#'+menuId).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');
	}else if (gType == 'fabless'){
		$("#sections ul li").children('.active').attr('class', 'nav-link');
		$("#idm ul li").children('.active').attr('class', 'nav-link');
		$("#fabless ul li").children('.active').attr('class', 'nav-link');
		$("#foundry ul li").children('.active').attr('class', 'nav-link');
		$("#enterprisesTitle").attr('class', 'nav-link active');
		$("#sectionsTitle").attr('class', 'nav-link');
    $('#fabless').attr('class', 'nav-item menu-is-opening menu-open');
    $('#fabless ul').attr('style', '');
      $('#'+menuId).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');
	}else if (gType == 'foundry'){
		$("#sections ul li").children('.active').attr('class', 'nav-link');
		$("#idm ul li").children('.active').attr('class', 'nav-link');
		$("#fabless ul li").children('.active').attr('class', 'nav-link');
		$("#foundry ul li").children('.active').attr('class', 'nav-link');
		$("#enterprisesTitle").attr('class', 'nav-link active');
		$("#sectionsTitle").attr('class', 'nav-link');
    $('#foundry').attr('class', 'nav-item menu-is-opening menu-open');
    $('#foundry ul').attr('style', '');
      $('#'+menuId).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');
	}else{
    if(menuId != ''){
      $("#sections ul li").children('.active').attr('class', 'nav-link');
      $("#idm ul li").children('.active').attr('class', 'nav-link');
      $("#fabless ul li").children('.active').attr('class', 'nav-link');
      $("#foundry ul li").children('.active').attr('class', 'nav-link');
      $("#sectionsTitle").attr('class', 'nav-link active');
      $("#enterprisesTitle").attr('class', 'nav-link');
      $('#'+menuId).attr('class', 'nav-link active');
      $('#directName').text('Sections');
    }
	}
  $('#titleName').text(decodeURI(decodeURIComponent(menuName)));
  console.log("menuId:", menuId);

  $(document).on("click", "#paging a", function(){   
    console.log('1');
  
    totalPage = Math.ceil(totalData / dataPerPage);    // 총 페이지 수
    pageGroup = Math.ceil(currentPage / pageCount);    // 페이지 그룹
    
    console.log('2');
    var $item = $(this);
    var $id = $item.attr("id");
    var menuId = $item.attr("menuId");
  
    var selectedPage = $item.text();
    console.log("id : " + $id);
  
    var last = pageGroup * pageCount;    // 화면에 보여질 마지막 페이지 번호
    if (last > totalPage)
        last = totalPage;
  
    var next = parseInt(currentPage) + 1; // 덧셈 연산 시 문자열로 변환된 후 실행되는 듯
    var prev = currentPage - 1;
    var first = last - (pageCount - 1);    // 화면에 보여질 첫번째 페이지 번호
  
    var fnext = last + 1;
    var fprev = first - 1;
  
    if ($id == "next") selectedPage = next;
    else if ($id == "prev") selectedPage = prev;
    else if ($id == "fnext") selectedPage = fnext; // 다음 페이지그룹의 1페이지
    else if ($id == "fprev") selectedPage = fprev; // 다음 페이지그룹의 마지막페이지
    else selectedPage = $id;
    
    console.log("click ====================");
    console.log("last : " + last);   // 마지막 페이지 번호
    console.log("first : " + first); // 첫 번째 페이지 번호
    console.log("next : " + next);   // 현재 페이지 + 1
    console.log("prev : " + prev);   // 현재 페이지 - 1
    console.log("fnext : " + fnext); // 다음 페이지 그룹의 첫 번째 페이지 번호
    console.log("fprev : " + fprev); // 다음 페이지 그룹의 마지막 페이지 번호
    console.log("click ====================");
  
    var baseUrl = 'http://127.0.0.1:5000/hash/'; 

    if(gType == 'idm'){
      menuUrl = 'all' + '/' + gMenuName + '/' + keyword + '/' + selectedPage;
    }else if (gType == 'fabless'){
      menuUrl = 'all' + '/' + gMenuName + '/' + keyword + '/' + selectedPage;
    }else if (gType == 'foundry'){
      menuUrl = 'all' + '/' + gMenuName + '/' + keyword + '/' + selectedPage;
    }else if (gType == 'sections') {
      menuUrl = gMenuName + '/' + 'all' + '/' + keyword + '/' + selectedPage;
    } else {
      menuUrl = 'all' + '/' + 'all' + '/' + keyword + '/' + selectedPage;
    }
    var url = baseUrl + menuUrl;
  
    getUrl(url, gType, gMenuName, menuId);
  });

});