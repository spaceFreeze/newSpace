var list1;
var list2;
var list3;

var totalData = 0;    
var currentPage = 1; 
var dataPerPage = 8;  
var pageCount = 5;    
var totalPage = 0;   
var pageGroup = 0;  

var gType;
var gMenuName;

function menuEvent(element, type, currentPage){

  var baseUrl = 'http://3.39.13.36:5000/'; 

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

  totalPage = Math.ceil(totalData / dataPerPage);    
  pageGroup = Math.ceil(currentPage / pageCount);    
  if (totalPage < pageCount) pageCount = totalPage;

  if(menuId == '' || menuId == undefined) menuId='all';

  var last = pageGroup * pageCount;  
  if (last > totalPage) 
    last = totalPage;   

  var next = parseInt(currentPage) + 1;
  var prev = currentPage - 1;
  var first = last - (pageCount - 1);  

  var fnext = last + 1; 
  var fprev = first - 1; 

  var $pingingView = $("#paging"); 

  var html = "";

  if (pageGroup > 1)
    html += "<a href=# menuId=" + menuId + " id='fprev' style=\"margin:20px;\"><<</a>";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  if (prev > 0)
    html += "<a href=# menuId=" + menuId + " id='prev' style=\"margin:20px;\"><</a> ";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  for (var i = first; i <= last; i++) {
    html += "<a href=# menuId=" + menuId + " id=" + i + " style=\"display:inline-block; margin:20px;\">" + i + "</a> ";
  }

  if (next <= totalPage)
    html += "<a href=# menuId=" + menuId + " id='next' style=\"margin:20px;\">></a>";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  if (last < totalPage)
    html += "<a href=# menuId=" + menuId + " id='fnext' style=\"margin:20px;\">>></a>";
  else
    html += "<a href=# style=\"margin:20px;\">  </a>";

  $("#paging").html(html);    
  $("#paging a").css({
    "color": "#A6A6A6",
    "font-size": "20"
  });
  $("#paging a#" + currentPage).css({  
    "text-decoration": "none",
    "color": "#007BFF",
    "font-size": "20",
    "font-weight": "bold"
  });    
}

function newsList1(list, type, menuName, menuId) {
  
    var genHtml = '';
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
        
        summaries_for_copy = '';
        (json.summaries).forEach(function(data, idx){
          if (data['summaries'+(idx+1)]) {
              genHtml += '		<p><font color="#007bff"><strong>'+ (idx+1) +'</strong></font>&nbsp;&nbsp;&nbsp;' + data['summaries'+(idx+1)] + '</p>';
              summaries_for_copy = summaries_for_copy + data['summaries'+(idx+1)] + ' ';
          }
        });

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
        genHtml += '         <i class="clip'+ idx +'" data-clipboard-text="' + summaries_for_copy + '"><i class="fas fa-share mr-1"></i>Copy</i></a>';

        genHtml += '         <script>';
        genHtml += '           var clipboard = new ClipboardJS( ".clip'+ idx +'" );';
        genHtml += '           clipboard.on( "success", function(e) {';
        genHtml += '             console.info("Text:", e.text);alert( "복사되었습니다." );';
        genHtml += '           } );';
        genHtml += '           clipboard.on( "error", function() {';
        genHtml += '             alert( "복사 실패" );';
        genHtml += '           } );';
        genHtml += '         </script>';

        genHtml += '		<span class="float-right text-muted">' + json.interest_cnt + ' interests - ' + json.com_cnt + ' comments</span>';
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
}
			
function newsList2(list, type, menuName, menuId){
    var genHtml = '';
 
    if (list2 == "nothing!") {
      var genHtml = '';
      genHtml += '<ul><li><a href="#" style="font-size: 20em">No Tags :)</a></li></ul>';
      $('#tags').html(genHtml);
      myCanvas();

      return;
    }
    list.forEach(function(json, idx){
      if (json.weight > 9) {
        json.weight = 9;
      } else if (json.weight < 2.5) {
        json.weight = 2.5;
      }
      genHtml += '<a href="#" onclick=window.open("keyword.html?type=' + gType + '&menuId=' + menuId + '&menuName=' + encodeURI(encodeURIComponent(gMenuName)) + '&keyword=' + encodeURI(encodeURIComponent(json.hashtag)) + '","_top") style="font-size: '+ json.weight +'em">'+ json.hashtag +'</a>';
    });

    $('#tags').html(genHtml);
    myCanvas();
}			

function newsList3(list){
    var genHtml = '';
    list.forEach(function(json, idx){
        genHtml += '<tr><td><font size="2em" color="#007bff"><strong>' + (idx+1) + '</strong></font></td>';
        genHtml += '<td><a href="' + json.url + '" target="_blank"><font size="2em" color="black">' + json.title + '</font></a></td>';
        genHtml += '<td><span class="badge bg-primary">' + json.interest_cnt + '</span></td></tr>';
    });

    $('#newList3').html(genHtml);
}		

function myCanvas(){
    if(!$('#myCanvas').tagcanvas({
    outlineColour: '#ff00ff',
    reverse: true,
    depth: 0.8,
    maxSpeed: 0.05,
    textFont: null,
    textColour: null,
    weightMode:'both',
    weight: true,
    weightGradient: {
     0:    '#f00',
     1:    '#00f'
    }
  },'tags')) {
    $('#myCanvasContainer').hide();
  }
}

function Request(){
  var requestParam ="";
  this.getParameter = function(param){
    var url = unescape(location.href);
    var paramArr = (url.substring(url.indexOf("?")+1,url.length)).split("&");
  
    for(var i = 0 ; i < paramArr.length ; i++){
      var temp = paramArr[i].split("="); 
  
      if(temp[0].toUpperCase() == param.toUpperCase()){
        requestParam = paramArr[i].split("=")[1];
        break;
      }
    }
    return requestParam;
  }
}

$(document).ready(function() {

  var request = new Request();

  var type = request.getParameter("type");
  gType = type;

  var menuName = request.getParameter("menuName");
  gMenuName = decodeURI(decodeURIComponent(menuName));

  var menuId = request.getParameter("menuId");

  var baseUrl = 'http://3.39.13.36:5000'; 

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

    totalPage = Math.ceil(totalData / dataPerPage);  
    pageGroup = Math.ceil(currentPage / pageCount);    
  
    var $item = $(this);
    var $id = $item.attr("id");
    var menuId = $item.attr("menuId");
  
    var selectedPage = $item.text();
  
    var last = pageGroup * pageCount;  
    if (last > totalPage)
        last = totalPage;
  
    var next = parseInt(currentPage) + 1;
    var prev = currentPage - 1;
    var first = last - (pageCount - 1);   
  
    var fnext = last + 1;
    var fprev = first - 1;
  
    if ($id == "next") selectedPage = next;
    else if ($id == "prev") selectedPage = prev;
    else if ($id == "fnext") selectedPage = fnext;
    else if ($id == "fprev") selectedPage = fprev; 
    else selectedPage = $id;

    var baseUrl = 'http://3.39.13.36:5000/'; 

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
  });
});