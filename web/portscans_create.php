<?php
require_once('common.php');

//  check login first
if (!already_login()) {
    error_jump();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="images/favicon.ico">

    <title>ICSScan</title>
    <!-- Documentation extras -->
    <link href="css/docs.min.css" rel="stylesheet">
    <!-- jquery -->
    <!-- <script type="text/javascript" charset="utf8" src="http://code.jquery.com/jquery-1.10.2.min.js"></script> -->
    <script src="js/jquery.min.js"></script>

    <link href="css/skins/line/blue.css" rel="stylesheet">
    <script src="js/jquery.icheck.min.js"></script>

    <!-- Bootstrap core JavaScript -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <script type="text/javascript" src="js/bootstrap.min.js"></script>

    <link href="css/live-search.css" rel="stylesheet">
    <script type="text/javascript" src="js/foot-2-live-search.js"></script>

    <link href="css/jsoneditor.css" rel="stylesheet">
    <script src="js/jquery.jsoneditor.js"></script>

    <!-- <script type="text/javascript" src="js/bootstrap-collapse.js"></script> -->
    <style type="text/css">
        a span{
            color: #555;
            text-decoration: none;
        }
        body{
            /*font-size: 16px;*/
        }
        .mcheck {
            width: 150px;
        }
        .panel {
            margin-top: 5px;
            margin-bottom: 5px;
        }
        blockquote {
            margin:0px;
            padding: 1px;
            font-size: 15px;
        }
        #legend {
            display: inline;
            margin-left: 30px;
        }
        #legend h2 {
            display: inline;
            font-size: 18px;
            margin-right: 20px;
        }
        #legend a {
            color: white;
            margin-right: 20px;
        }
        #legend span {
            padding: 2px 4px;
            -webkit-border-radius: 5px;
            -moz-border-radius: 5px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            text-shadow: 1px 1px 1px black;
            background-color: black;
        }
        #legend .string  { background-color: #009408; }
        #legend .array   { background-color: #2D5B89; }
        #legend .object  { background-color: #E17000; }
        #legend .number  { background-color: #497B8D; }
        #legend .boolean { background-color: #B1C639; }
        #legend .null    { background-color: #B1C639; }

        #expander {
            cursor: pointer;
            margin-right: 20px;
        }
    </style>
    
    <script>
        function task_create(){
            // check target
            if ($("#target").val() == '') {alert("target cannot be empty");return;};

            //
            var str_data='';
            var radio='';
            $("#dlg_form input,textarea,select").each(function(){
                if($(this).attr("name") != undefined && $(this).attr("type") != "radio"){
                    if ($(this).attr("type")=="checkbox") {
                        str_data += $(this).attr("name") + "=" + ($(this).attr("checked")=="checked"?1:0) + "&";
                    }
                    else{
                        str_data += $(this).attr("name") + "=" + $(this).val() + "&";
                    }
                }
            });
            if ($('input:radio:checked').val() != undefined){
                str_data += "config[global][choose]=" + $('input:radio:checked').val();
            }
            
            alert("Scanning , please wait !");

            $.ajax({
                type: "POST",
                url: "portscans_add.php",
                data: str_data,
                success: function(msg){
                    if (msg == true) {alert('PortScans Success');}
                    else {alert('PortScans Faild');}
                    location.href = 'portscans.php';
                }
            });
        }


        $(document).ready(function () {

            // $('.input').iCheck({
            // 	checkboxClass: 'icheckbox_minimal-blue',
            // 	radioClass: 'iradio_minimal-blue',
            // 	increaseArea: '20%' // optional
            // });

            $.ajax({
                type: "POST",
                url: "dist_search.php",
                data: "status=0",
                dataType: "json",
                success: function(data){
                    console.log(data.data);
                    dists = data.data;
                    if (dists.length) {
                        var html = '';
                        console.log('yes');
                        for (var i = dists.length - 1; i >= 0; i--) {
                            dist = dists[i];
                            if (dist[5]=='1') {
                                html += '<span class="label label-info">'+dist[1]+'@'+dist[3]+'</span>&nbsp;';
                            }
                        };
                        $('#dists').html(html);
                        $('#submit').removeClass('disabled');
                    }
                }
            });
        });

    </script>
</head>


<body>

<!-- Main jumbotron for a primary marketing message or call to action -->
<div class="container">
    <h1>
        <a href="index.php">
            <!-- <small><span class="glyphicon glyphicon-home"></span></small> -->
            <span class="glyphicon glyphicon-home"></span>
        </a>
        <a href="javascript:history.back()">
            <span class="glyphicon glyphicon-circle-arrow-left"></span>
        </a>
        Create PortScans
        <!-- &nbsp;Plugin Code -->
        <!-- <a class="glyphicon glyphicon-circle-arrow-left" id="plugin_goback" href="javascript:history.back()"></a>&nbsp; -->
    </h1>
    <div class="form" id="dlg_form">
        <div class="panel panel-default form-group">
            <div class="panel-heading "><strong>IP Address</strong></div>
            <div class="panel-body collapse in" id="modules" style="padding:5px">
                <div class="content">
                    <div class="row">
                        <div class="col-md-6" style="margin:0px">
                            <textarea class="form-control" id="target" name="config[global][ip]" size="50" rows="3" placeholder="0.0.0.0,1.1.1.1.1"></textarea>
                        </div>
                        <div class="col-md-6">
                            <div class="list-group" style="margin:0px">
                                <h4 class="list-group-item-heading">Notice: Input ip address</h4>
                                <p class="list-group-item-text">Such as: 0.0.0.0
                                    <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.0.0.0,1.1.1.1.1
                                    <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.0.0.0-255.255.255.255
                             </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="panel panel-default form-group">
            <div class="panel-heading" data-toggle="collapse" data-target="#options" aria-expanded="true" aria-controls="options"><strong>Scans Information</strong></div>
            <div class="panel-body collapse in" id="options">
                <div class="content" style="overflow: hidden; display: block;">
                    <div class="row">
                        <div class="col-md-2">
                            <blockquote>Info</blockquote>
                        </div>
                        <div class="col-md-10 form-inline">
                            <div>
                                Threads&nbsp;&nbsp;&nbsp;
                                <input type="text" class="form-control" name="config[global][threads]" size="4" value=10>
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Timeout&nbsp;&nbsp;&nbsp;
                                <input type="text" class="form-control" name="config[global][timeout]" size="4" value=5>
                            </div>
                        </div>
                    </div>
                    <div class="row form-line">
                        <div class="col-md-2">
                            <blockquote>Types</blockquote>
                        </div>
                        <div class="col-md-10">
                            <input type="radio" name="config[global][choose]" value="common"> common
                            <input type="radio" name="config[global][choose]" value="ics"> ics
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div>
            <button class="btn btn-warning btn-default disabled" id="submit" onclick="task_create()">
                <span class="glyphicon glyphicon-flash"></span>
                Scan it!
            </button>
        </div>
        </form>
        <hr>
        <footer>
            <p>© ICS-426-2016</p>
        </footer>
    </div>
    <!-- ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
</body>
</html>