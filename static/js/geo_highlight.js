$(document).ready(function () {
	$("#templatemo_geomenu li a").click(function () {
		
        
        $("#templatemo_geomenu li a").removeClass('current');
		$(this).addClass('current');
        
		return false;
		/* window.location.href = this.getAttribute('href'); */
	});
	
	
});




