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

  $('#titleName').text(menuName);

  if (currentPage == undefined) currentPage = '1';
  var menuId = $(element).attr('id');

	if(gType == 'idm'){
		$("#sections ul li").children('.active').attr('class', 'nav-link');
		$("#idm ul li").children('.active').attr('class', 'nav-link');
		$("#fabless ul li").children('.active').attr('class', 'nav-link');
		$("#foundry ul li").children('.active').attr('class', 'nav-link');
		$("#enterprisesTitle").attr('class', 'nav-link active');
		$("#sectionsTitle").attr('class', 'nav-link');
		$(element).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');

    menuUrl = 'all' + '/' + gMenuName + '/' + currentPage;
	}else if (gType == 'fabless'){
		$("#sections ul li").children('.active').attr('class', 'nav-link');
		$("#idm ul li").children('.active').attr('class', 'nav-link');
		$("#fabless ul li").children('.active').attr('class', 'nav-link');
		$("#foundry ul li").children('.active').attr('class', 'nav-link');
		$("#enterprisesTitle").attr('class', 'nav-link active');
		$("#sectionsTitle").attr('class', 'nav-link');
		$(element).attr('class', 'nav-link active');
    $('#directName').text('Enterprises');

    menuUrl = 'all' + '/' + gMenuName + '/' + currentPage;
	}else if (gType == 'foundry'){
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
  getUrl(url, type, menuName, menuId);
}

function getUrl(url, type, menuName, menuId) {
	
    if(type == undefined) gType = 'all';
    if(menuName == undefined) gMenuName = 'all';

    loadItems(url).then((items) => {
      itemsStr = JSON.stringify(items); 
      itemsStr = JSON.parse(itemsStr);   

      totalData = itemsStr.list1.total;
      if (totalData)
      currentPage = itemsStr.list1.page;

      list1 = itemsStr.list1.list;
      list2 = itemsStr.list2;
      list3 = itemsStr.list3;

      newsList1(list1, type, menuName, menuId);
      paging(totalData, dataPerPage, pageCount, currentPage, menuId);
      newsList2(list2, type, menuName, menuId);
      newsList3(list3); 
    })
    .catch(function(error) {
        console.log('There has been a problem with your fetch operation: ', error);
        $('#paging').html('');
      });
}

function loadItems(url) {
    return fetch(url)
        .then((response) => response.json()) 
        .then((json) => json)
}

function paging(totalData, dataPerPage, pageCount, currentPage, menuId) {

  totalPage = Math.ceil(totalData / dataPerPage);    // 총 페이지 수
  pageGroup = Math.ceil(currentPage / pageCount);    // 페이지 그룹

  if (totalPage < pageCount) pageCount = totalPage;

  if(menuId == '' || menuId == undefined) menuId='all';
  console.log("====================");
  console.log("totalData:", totalData)
  console.log("totalPage :",  totalPage);  // 총 페이지 수
  console.log("pageGroup :", pageGroup);  // 현재 페이지 그룹
  console.log("currentPage :", currentPage);  // 현재 페이지 수

  var last = pageGroup * pageCount;    // 마지막 페이지 번호  // pageCount: 5
  if (last > totalPage)  // 마지막 그룹의 페이지 수가 다 못 채워질 경우(ex. 총 12페이지)
    last = totalPage;    // 마지막 페이지 번호 = 12

  var next = parseInt(currentPage) + 1;
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
    console.log('list1 >> '+list)
    if (list1 == "nothing!") {
      var genHtml = '';
      genHtml += '<div class="display-4" style="margin: auto;display: inline-block; position:absolute; left:50%; top:50%; margin-left:-150px; margin-top:-150px;">No News!</div>';
      $('#newsList1').html(genHtml);

      return;
    }
        genHtml += '<div class="row">';
    list.forEach(function(json, idx){

        fiusrc = '';
        if (json.img_url == 'none') {
            fiusrc = 'dist/img/noimg3.png';
        } else {
            fiusrc = json.img_url;
        }

        // console.log('newsList1 : ' + idx);
        if(idx%2 == 0){
        genHtml += '<div class="row">';
        }
        
        genHtml += '  <div class="col-md-6">';
        genHtml += '	<!-- Box Comment -->';
        genHtml += '	<div class="card card-widget">';
        genHtml += '	  <div class="card-header">';
        genHtml += '		<div class="user-block">';
        genHtml += '		  <img class="img-circle" src="' + json.logo_url + '" alt="Logo Image">';
        genHtml += '		  <span class="username"><a href="' + json.press_url + '" target="_blank">' + json.press + '</a></span>';
        genHtml += '		  <span class="description">' + json.date + '</span>';
        genHtml += '		</div>';
        genHtml += '		<!-- /.user-block -->';
        genHtml += '		<div class="card-tools">';
        genHtml += '		  <button type="button" class="btn btn-tool" data-card-widget="collapse">';
        genHtml += '			<i class="fas fa-minus"></i>';
        genHtml += '		  </button>';
        genHtml += '		  <button type="button" class="btn btn-tool" data-card-widget="remove">';
        genHtml += '			<i class="fas fa-times"></i>';
        genHtml += '		  </button>';
        genHtml += '		</div>';
        genHtml += '		<!-- /.card-tools -->';
        genHtml += '	  </div>';
        genHtml += '	  <!-- /.card-header -->';
        genHtml += '	  <div class="card-body">';
        genHtml += '		<!-- post text -->';
        
        genHtml += '		<p>' + json.summaries + '</p>';
        
        genHtml += '		<!-- Attachment -->';
        genHtml += '		<div class="attachment-block clearfix" style="position: relative; overflow: auto;">';
        
        genHtml += '		  <img class="attachment-img" src="' + fiusrc + '" alt="News Image"">';

        genHtml += '		  <div class="attachment-pushed" style="position: absolute; top: 11px;">';
        genHtml += '			<h4 class="attachment-heading"><a href="' + json.url + '" target="_blank"><font size="4em">' + json.title + '</font></a></h4>';
        
        genHtml += '            <span style="line-height:30%"><br></span>';
        genHtml += '			<div class="attachment-text">';
        genHtml += '			  <font size="2pt">' + json.content + '...&nbsp;</font><a href="' + json.url + '" target="_blank">more</a>';
        genHtml += '			</div>';
        genHtml += '			<!-- /.attachment-text -->';
        genHtml += '		  </div>';
        genHtml += '		  <!-- /.attachment-pushed -->';
        genHtml += '		</div>';
        genHtml += '		<!-- /.attachment-block -->';
        
        genHtml += '		<!-- Social sharing buttons -->';
        genHtml += '		<a style="cursor:pointer;" class="link-black text-sm mr-2" >';
        genHtml += '         <i class="clip'+ idx +'" data-clipboard-text="' + json.summaries + '"><i class="fas fa-share mr-1"></i>Copy</i></a>';

        genHtml += '         <script>';
        genHtml += '           var clipboard = new ClipboardJS( ".clip'+ idx +'" );';
        genHtml += '           clipboard.on( "success", function(e) {';
        genHtml += '             console.info("Text:", e.text);alert( "복사되었습니다." );';
        genHtml += '           } );';
        genHtml += '           clipboard.on( "error", function() {';
        genHtml += '             alert( "복사 실패" );';
        genHtml += '           } );';
        genHtml += '         </script>';

        genHtml += '		<span class="float-right text-muted">' + json.like_cnt + ' likes - ' + json.com_cnt + ' comments</span>';
        genHtml += '	  </div>';
        genHtml += '	  <!-- /.card-body -->';
        genHtml += '	  <div class="card-footer card-comments">';
        
        (json.hashtag).forEach(function(data, idx){
            genHtml += '		<button type="button" class="btn btn-default btn-sm" onclick=window.open("keyword.html?type=' + gType + '&menuId=' + menuId + '&menuName=' + encodeURI(encodeURIComponent(gMenuName)) + '&keyword=' + encodeURI(encodeURIComponent(data['hash'+(idx+1)])) + '","_top")>' + '#' + data['hash'+(idx+1)] + '</button>';
        });
        
        genHtml += '	  </div>';
        genHtml += '	</div>';
        genHtml += '	<!-- /.card -->';
        genHtml += '  </div>';
        
        if(idx != 0 && idx%2 != 0){
        genHtml += '</div>';
        genHtml += '<!-- /.row -->';
        }
    });
    
    $('#newsList1').html(genHtml);
    //copy();
    // paging(totalData, dataPerPage, pageCount, currentPage);
}
			
function newsList2(list, type, menuName, menuId){
    var genHtml = '';

    console.log('list2 >> '+list)
    if (list2 == "nothing!") {
      var genHtml = '';
      genHtml += '<ul><li><a href="#" style="font-size: 20em">No Tags :)</a></li></ul>';
      $('#tags').html(genHtml);
      myCanvas();

      return;
    }
    list.forEach(function(json, idx){
        genHtml += '<a href="#" onclick=window.open("keyword.html?type=' + gType + '&menuId=' + menuId + '&menuName=' + encodeURI(encodeURIComponent(gMenuName)) + '&keyword=' + encodeURI(encodeURIComponent(json.text)) + '","_top") style="font-size: '+ json.size +'em">'+ json.text +'</a>';
    });

    $('#tags').html(genHtml);
    myCanvas();
}			

function newsList3(list){
    var genHtml = '';
console.log('list3 >> '+list)
    list.forEach(function(json, idx){
        genHtml += '<tr><td><font size="2em" color="#007bff"><strong>' + (idx+1) + '</strong></font></td>';
        genHtml += '<td><a href="' + json.url + '" target="_blank"><font size="2em" color="black">' + json.title + '</font></a></td>';
        genHtml += '<td><span class="badge bg-primary">' + json.recom_react_cnt + '</span></td></tr>';
    });

    $('#newList3').html(genHtml);
}		

function myCanvas(){
    if(!$('#myCanvas').tagcanvas({
    //textColour: '#ff0000',
    outlineColour: '#ff00ff',
    reverse: true,
    depth: 0.8,
    maxSpeed: 0.05,
    textFont: null,
    textColour: null,
    weightMode:'both',
    weight: true,
    weightGradient: {
     0:    '#f00', // red
     //0.33: '#ff0', // yellow
     //0.66: '#0f0', // green
     1:    '#00f'  // blue
    }
  },'tags')) {
    $('#myCanvasContainer').hide();
  }
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
  //myCanvas();
  //copy(); 
  // getUrl('dist/json.json');

  // Request 객체 생성
  var request = new Request();

  var type = request.getParameter("type");
  gType = type;
  // if(type == undefined) gType = 'all';

  var menuName = request.getParameter("menuName");
  gMenuName = decodeURI(decodeURIComponent(menuName));
  // if(menuName == undefined) gMenuName = 'all';

  var menuId = request.getParameter("menuId");
  console.log('type : '+ gType);
  console.log('menuName : '+ gMenuName);

  var baseUrl = 'http://127.0.0.1:5000';

  var url = '';
  if (type == 'sections') {
    url = baseUrl + '/' + gMenuName + '/' + 'all' + '/' + currentPage;
  } else if (type == 'idm') {
    url = baseUrl + '/' + 'all' + '/' + gMenuName + '/' + currentPage;
  } else if (type == 'fabless') {
    url = baseUrl + '/' + 'all' + '/' + gMenuName + '/' + currentPage;
  } else if (type == 'foundry') {
    url = baseUrl + '/' + 'all' + '/' + gMenuName + '/' + currentPage;
  } else {
    url = baseUrl + '/' + 'all' + '/' + 'all' + '/' + currentPage;
  }
  
  // getUrl(baseUrl);
  console.log("url:", url);
  console.log("menuId:", menuId);

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
  if(menuName == '')menuName='전체';

  $('#titleName').text(decodeURI(decodeURIComponent(menuName)));
  getUrl(url, gType, gMenuName, menuId); 

  $(document).on("click", "#paging a", function(){   

    totalPage = Math.ceil(totalData / dataPerPage);    // 총 페이지 수
    pageGroup = Math.ceil(currentPage / pageCount);    // 페이지 그룹
  
    var $item = $(this);
    var $id = $item.attr("id");
    var menuId = $item.attr("menuId");
  
    var selectedPage = $item.text();
    console.log("id : " + $id);
  
    var last = pageGroup * pageCount;    // 화면에 보여질 마지막 페이지 번호
    if (last > totalPage)
        last = totalPage;
  
    var next = parseInt(currentPage) + 1; // 덧셈 연산 시 문자열로 변환된 후 실행되는 듯(?)
    var prev = currentPage - 1;
    var first = last - (pageCount - 1);    // 화면에 보여질 첫번째 페이지 번호
  
    var fnext = last + 1;
    var fprev = first - 1;
  
    if ($id == "next") selectedPage = next;
    else if ($id == "prev") selectedPage = prev;
    else if ($id == "fnext") selectedPage = fnext; //다음 페이지그룹의 1페이지
    else if ($id == "fprev") selectedPage = fprev; //다음 페이지그룹의 마지막페이지
    else selectedPage = $id;

    console.log("click ====================");
    console.log("last : " + last);   // 마지막 페이지 번호
    console.log("first : " + first); // 첫 번째 페이지 번호
    console.log("next : " + next);   // 현재 페이지 + 1
    console.log("prev : " + prev);   // 현재 페이지 - 1
    console.log("fnext : " + fnext); // 다음 페이지 그룹의 첫 번째 페이지 번호
    console.log("fprev : " + fprev); // 다음 페이지 그룹의 마지막 페이지 번호
    console.log("click ====================");

    // paging(totalData, dataPerPage, pageCount, selectedPage);
  
    // var baseUrl = 'http://127.0.0.1:5000/all/all/'+selectedPage;
    var baseUrl = 'http://127.0.0.1:5000/'; 
  
    if(gType == 'idm'){
      menuUrl = 'all' + '/' + gMenuName + '/' + selectedPage;
    }else if (gType == 'fabless'){
      menuUrl = 'all' + '/' + gMenuName + '/' + selectedPage;
    }else if (gType == 'foundry'){
      menuUrl = 'all' + '/' + gMenuName + '/' + selectedPage;
    }else if (gType == 'sections'){
      menuUrl = gMenuName + '/' + 'all' + '/' + selectedPage;
    } else {
      menuUrl = 'all' + '/' + 'all' + '/' + selectedPage;
    }
    var url = baseUrl + menuUrl;
  
    getUrl(url, gType, gMenuName, menuId);
    // paging(totalData, dataPerPage, pageCount, selectedPage);
  });

});