package com.futurepath.repo;

import com.futurepath.db.Db;

import java.sql.*;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

public class RunRepository {

  public void save(String requestJson, String responseJson) {
    String sql = "INSERT INTO runs(created_at, request_json, response_json) VALUES(?,?,?)";
    try (Connection c = Db.connect();
         PreparedStatement ps = c.prepareStatement(sql)) {
      ps.setString(1, Instant.now().toString());
      ps.setString(2, requestJson);
      ps.setString(3, responseJson);
      ps.executeUpdate();
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  public List<String> lastResponses(int limit) {
    String sql = "SELECT created_at, response_json FROM runs ORDER BY id DESC LIMIT ?";
    List<String> out = new ArrayList<>();
    try (Connection c = Db.connect();
         PreparedStatement ps = c.prepareStatement(sql)) {
      ps.setInt(1, limit);
      try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
          out.add(rs.getString(1) + " | " + rs.getString(2));
        }
      }
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
    return out;
  }
}
