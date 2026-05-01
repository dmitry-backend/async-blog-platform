import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import styles from "./Header.module.css";

const Header = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <header className={styles.header}>
      <nav className={styles.nav}>
        <Link to="/">HOME</Link>
        
        {user ? (
          <>
            <Link to="/create-post">NEW POST</Link>
            
            <span className={styles.user}>{user.email}</span>
            <button onClick={logout}>LOGOUT</button>
          </>
        ) : (
          <>
            <Link to="/login">LOGIN</Link>
            <Link to="/register">REGISTER</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
