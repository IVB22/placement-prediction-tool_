package com.futurepath.service;

import com.futurepath.config.AppConfig;
import com.futurepath.model.MatchRequest;
import com.futurepath.model.MatchResponse;
import com.futurepath.util.JsonUtil;

import okhttp3.*;
import java.time.Duration;

public class MlApiService {
  private final OkHttpClient http = new OkHttpClient.Builder()
      .connectTimeout(Duration.ofSeconds(30))
      .readTimeout(Duration.ofSeconds(180))
      .writeTimeout(Duration.ofSeconds(60))
      .callTimeout(Duration.ofSeconds(180))
      .build();

  public MatchResponse match(MatchRequest req) {
    String url = AppConfig.ML_BASE_URL + AppConfig.MATCH_PATH;

    RequestBody body = RequestBody.create(
        JsonUtil.toJson(req),
        MediaType.parse("application/json")
    );

    Request request = new Request.Builder()
        .url(url)
        .post(body)
        .build();

    try (Response resp = http.newCall(request).execute()) {
      if (!resp.isSuccessful()) {
        throw new RuntimeException("ML API error: " + resp.code());
      }
      String json = resp.body().string();
      return JsonUtil.fromJson(json, MatchResponse.class);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
