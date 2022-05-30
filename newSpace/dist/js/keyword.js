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
    
  var url = baseUrl + menuUrl;

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

  totalPage = Math.ceil(totalData / dataPerPage);    
  pageGroup = Math.ceil(currentPage / pageCount);   

  if (totalPage < pageCount) pageCount = totalPage;

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
    list.forEach(function(json, idx){
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
        
        (json.summaries).forEach(function(data, idx){
          if (data['summaries'+(idx+1)]) {
              genHtml += '		<p><font color="#007bff"><strong>'+ (idx+1) +'</strong></font>&nbsp;&nbsp;&nbsp;' + data['summaries'+(idx+1)]  + '</p>';
          }
        });
        
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

  var keyword = request.getParameter("keyword");
  var type = request.getParameter("type");
  var menuId = request.getParameter("menuId");
  gType = type;
  var menuName = request.getParameter("menuName");
  gMenuName = menuName;

  var baseUrl = 'http://3.39.13.36:5000/hash'; 

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

    var baseUrl = 'http://3.39.13.36:5000/hash/'; 

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