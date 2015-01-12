<?php

 /**
  * settings.php: contains various php configuration settings.
  */

 /**
  * Database: when instantiating this class, or defining any of the class variables,
  *           make sure they are defined within the DBMS. This can be achieved via
  *           the terminal console (or phpMyAdmin):
  *
  *               $ mysql -u root -p
  *               MariaDB> CREATE USER 'authenticated'@'localhost' IDENTIFIED BY
  *                   ->'password';
  *               MariaDB> GRANT, CREATE, DELETE, DROP, EXECUTE, SELECT, SHOW
  *                   -> DATABASES ON *.* TO 'authenticated'@'localhost';
  *               MariaDB> FLUSH PRIVILEGES;
  */
  class Database {

  /**
   * Constructor
   */
    public function __construct() {
      $this->db_host     = 'localhost';
      $this->db_username = 'authenticated';
      $this->db_password = 'password';
    }

  /**
   * get_db_host: get the database host
   */
    protected function get_db_host() {
      return $this->db_host;
    }

  /**
   * get_db_username: get the database username
   */
    protected function get_db_username() {
      return $this->db_username;
    }

  /**
   * get_db_password: get the database user password
   */
    protected function get_db_password() {
      return $this->db_password;
    }

  /**
   * set_db_host: define the database host
   */
    protected function set_db_host($host) {
      $this->db_host = $host;
    }

  /**
   * set_db_username: define the database user
   */
    protected function set_db_username($user) {
      $this->db_username = $user;
    }

  /**
   * set_db_password: define the database password
   */
    protected function set_db_password($pwd) {
      $this->db_password = $pwd;
    }

 }
