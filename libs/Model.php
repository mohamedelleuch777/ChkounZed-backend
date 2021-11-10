<?php



class Model {
    public $db;
    function __construct() {
        // instantiate database
        $this->db = new MySQL_Query("remotemysql.com","O4pKtnrYIk","hd0iDziUDK","O4pKtnrYIk");
        return $this->db;
    }

    function ExecQuery($sqlCode) {
        $res = $this->db->ExecSql($sqlCode);
        if(!$res) {
            return $this->db->GetError();
        }
        $resList = [];
        while($this->db->AvailableResult()) {
            array_push($resList, $this->db->GetObject());
        }
        return $resList;
    }

    function ExecQueryNoFetch($sqlCode) {
        $res = $this->db->ExecSql($sqlCode);
        return $res;
    }
}