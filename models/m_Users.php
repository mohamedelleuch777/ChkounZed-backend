<?php

class m_Users extends Model {
    private $db_conn;
    function __construct () {
        $this->db_conn = parent::__construct();
    }

    function GetAllUsers() {
        $sql = 'SELECT * FROM `Users`';;
        return $this->ExecQuery($sql);
    }

    function GetUserByEmail($output) {
        $email = $output['email'];
        $sql = 'SELECT * FROM `Users` WHERE `email`="'.$email.'"';
        return $this->ExecQuery($sql);
    }

    function GetUserByUsername($output) {
        $username = $output['username'];
        $sql = 'SELECT * FROM `Users` WHERE `username`="'.$username.'"';
        return $this->ExecQuery($sql);
    }

    function CreateUser($output) {
        $username           = $output['username'];
        $email              = $output['email'];
        $firstname          = $output['firstname'];
        $lastname           = $output['lastname'];
        $birthday           = $output['birthday'];
        $creationDate       = $output['creationDate'];
        $password           = $output['password'];
        $sql = "INSERT INTO `Users` (`id`, `username`, `email`, `firstname`, `lastname`, `birthday`, `creationDate`, `password`)
                VALUES (NULL, '$username', '$email', '$firstname', '$lastname', '$birthday', '$creationDate', '$password');";
        return $this->ExecQueryNoFetch($sql);
    }


}