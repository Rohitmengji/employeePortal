function printdata() 
{
	{
		var printContents = document.getElementById("print").innerHTML;
		var originalContents = document.body.innerHTML;
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		if(dd<10) 
		{
    		dd='0'+dd;
		} 
		if(mm<10) 
		{
		    mm='0'+mm;
		} 
		today = dd+'/'+mm+'/'+yyyy;

		document.body.innerHTML = "<html><head></head><body><table border='1' align='center' style='color:black;' width='100px'><tr><td colspan='2'><center><font size='+2' color='green'>Adarsh Resturant</font><br/><font size='+1'>SB temple Road Vittal Nagar<br/>Kalaburagi</font></center><br/><center><hr/></td></tr><tr><td align='right'>Bill No.:.............&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Date:"+today+"</td></tr><tr><td></br>Name:........................</td></tr><tr><td width='100%' height'100%'>"+printContents.replace('th','td')+"</td></tr></table></center></body></html>";
 		window.print();
		document.body.innerHTML = originalContents; 
	 	document.getElementById("btnprint").style.visibility="hidden";
	}
}
