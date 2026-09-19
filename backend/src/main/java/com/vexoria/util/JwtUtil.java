package com.vexoria.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.vexoria.models.User;

import java.time.Instant;
import java.time.temporal.ChronoUnit;

public class JwtUtil {
    private static final String SECRET_KEY = System.getenv().getOrDefault("JWT_SECRET", "vexoria_hackathon_team_finder_secret_key_2026");
    private static final Algorithm ALGORITHM = Algorithm.HMAC256(SECRET_KEY);
    private static final JWTVerifier VERIFIER = JWT.require(ALGORITHM).build();

    public static String generateToken(User user) {
        return JWT.create()
                .withSubject(user.getId())
                .withClaim("email", user.getEmail())
                .withClaim("name", user.getName())
                .withExpiresAt(Instant.now().plus(7, ChronoUnit.DAYS))
                .sign(ALGORITHM);
    }

    public static DecodedJWT verifyToken(String token) throws JWTVerificationException {
        return VERIFIER.verify(token);
    }

    public static String getUserId(DecodedJWT jwt) {
        return jwt.getSubject();
    }

    public static String getEmail(DecodedJWT jwt) {
        return jwt.getClaim("email").asString();
    }
}
