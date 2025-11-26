import React, { useState, useEffect } from "react";
import { getCookie } from "../../helpers/getCookie";
import "../../styles/login.css";

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('logout') === 'true') {
      setSuccessMessage("Você se desconectou com sucesso");
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMessage("");
    setIsLoading(true);

    const csrftoken = getCookie("csrftoken");

    try {
      const response = await fetch("/api/auth/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        onLoginSuccess();
      } else {
        setError(data.error || "Erro ao fazer login. Tente novamente.");
      }
    } catch (error) {
      console.error("Erro ao fazer login:", error);
      setError("Erro de conexão. Verifique sua internet e tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    // Adicionamos este wrapper para conter os estilos da página de login
    <div className="login-wrapper">
      <div className="container" id="tela-login">
        <h2>Vyzio</h2>

        {successMessage && (
          <div className="mensagem sucesso">
            <i className="fas fa-circle-check"></i>
            <span>{successMessage}</span>
          </div>
        )}

        {error && (
          <div className="mensagem erro">
            <i className="fas fa-circle-xmark"></i>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <i className="fas fa-user input-icon"></i>
            <input
              type="text"
              id="username"
              name="username"
              placeholder="Usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
              autoFocus
            />
          </div>

          <div className="input-group">
            <i className="fas fa-lock input-icon"></i>
            <input
              type={showPassword ? "text" : "password"}
              id="password"
              name="password"
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
            />
            <i
              className={showPassword ? "fas fa-eye-slash toggle-password" : "fas fa-eye toggle-password"}
              title={showPassword ? "Ocultar senha" : "Mostrar senha"}
              onClick={togglePasswordVisibility}
            ></i>
          </div>

          <button type="submit" disabled={isLoading} className="btn">
            {isLoading ? (
              <>
                <i className="fas fa-spinner fa-spin"></i> Entrando...
              </>
            ) : (
              <>
                <i className="fas fa-sign-in-alt"></i> Entrar
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
