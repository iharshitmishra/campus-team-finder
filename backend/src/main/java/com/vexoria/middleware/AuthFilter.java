package com.vexoria.middleware;

import com.auth0.jwt.interfaces.DecodedJWT;
import com.vexoria.util.JwtUtil;
import io.javalin.http.Context;
import io.javalin.http.UnauthorizedResponse;

public class AuthFilter {

    public static void filter(Context ctx) {
        String path = ctx.path();
        String method = ctx.method().name();

        // Browser CORS preflight requests must ALWAYS pass through
        if ("OPTIONS".equalsIgnoreCase(method)) {
            return;
        }

        // Check if route requires auth
        boolean needsAuth = false;

        if (path.startsWith("/api/users/me") || path.startsWith("/api/requests")) {
            needsAuth = true;
        } else if (path.startsWith("/api/teams")) {
            // GET /api/teams and GET /api/teams/:id are public
            if ("POST".equalsIgnoreCase(method) || "PUT".equalsIgnoreCase(method) || "DELETE".equalsIgnoreCase(method)) {
                needsAuth = true;
            }
        }

        if (!needsAuth) {
            return;
        }

        String authHeader = ctx.header("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            ctx.status(401).json(java.util.Map.of("error", "Missing or invalid Authorization header"));
            throw new UnauthorizedResponse("Missing or invalid Authorization header");
        }

        String token = authHeader.substring(7).trim();
        try {
            DecodedJWT jwt = JwtUtil.verifyToken(token);
            ctx.attribute("userId", JwtUtil.getUserId(jwt));
            ctx.attribute("userEmail", JwtUtil.getEmail(jwt));
        } catch (Exception e) {
            ctx.status(401).json(java.util.Map.of("error", "Invalid or expired token"));
            throw new UnauthorizedResponse("Invalid or expired token");
        }
    }
}
