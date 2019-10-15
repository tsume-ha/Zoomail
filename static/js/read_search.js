function searchformsubmit(){
	var q;
	var is_kaisei;
	var is_zenkai;
	var is_midoku;
	var is_marked;
	var paramlist = [];
	if (document.advanced_search.text.value != ""){
		q = encodeURIComponent(document.advanced_search.text.value);
		paramlist.push('q='+q);
	}
	if (document.advanced_search.is_kaisei.checked != ""){
		is_kaisei = 'true';
		paramlist.push('is_kaisei='+is_kaisei);
	}
	if (document.advanced_search.is_zenkai.checked != ""){
		is_zenkai = 'true';
		paramlist.push('is_zenkai='+is_zenkai);
	}
	if (document.advanced_search.is_midoku.checked != ""){
		is_midoku = 'true';
		paramlist.push('is_midoku='+is_midoku);
	}
	if (document.advanced_search.is_marked.checked != ""){
		is_marked = 'true';
		paramlist.push('is_marked='+is_marked);
	}
	console.log(paramlist);
	var parameter = '?' + paramlist.join('&');
	window.location.search = parameter;
	return false;
}