package com.futurepath.util;

import com.fasterxml.jackson.databind.ObjectMapper;

public final class JsonUtil {
  private static final ObjectMapper M = new ObjectMapper();
  private JsonUtil() {}

  public static String toJson(Object o) {
    try { return M.writeValueAsString(o); }
    catch (Exception e) { throw new RuntimeException(e); }
  }

  public static <T> T fromJson(String s, Class<T> cls) {
    try { return M.readValue(s, cls); }
    catch (Exception e) { throw new RuntimeException(e); }
  }
}
