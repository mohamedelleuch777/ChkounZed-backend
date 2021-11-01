<?php

class MySQL_Query {
    public $conn = null;
    private $result = null;
    private $obj = null;
  
    public function __construct($servername, $username, $password, $dbName) {
      $this->SetupCnxDB($servername, $username, $password, $dbName);
    }
  
    public function SetupCnxDB($servername, $username, $password, $dbName) {
      $this->$conn = new mysqli($servername, $username, $password, $dbName);
      if ($this->$conn->connect_error) {
        return false;
      }
      return true;
    }
  
    public function ExecSql($sql) {
      return ($this->result = $this->$conn->query($sql));
    }
    
    public function ExecMultiSql($sql) {
      return ($this->result = $this->$conn->multi_query($sql));
    }
    
    public function MultiQueryStoreResult() {
      return ($this->result = $this->$conn->store_result());
    }
  
    public function Length() {
      return $this->result->num_rows;
    }
  
    public function AvailableResult() {
      return ($this->obj = $this->result->fetch_object());
    }
  
    public function GetObject() {
      return $this->obj;
    }
  
    public function GetConnectionError() {
      return $this->$conn->connect_error;
    }
  
    public function GetError() {
      return $this->$conn->error;
    }
  }