<?php



class Model {
    private $db;
    function __construct() {
        // instantiate database
        $db = new MySQL_Query("127.0.0.1","root","password","chkoun_zed");
    }

    function GetUser() {
        
    }
}