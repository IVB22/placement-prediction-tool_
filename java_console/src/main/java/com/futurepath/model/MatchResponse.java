package com.futurepath.model;

import java.util.List;
import java.util.Map;

public class MatchResponse {
  public String mode;
  public double placement_probability;

  public Integer role_fit_score;
  public Integer resume_ats_score;
  public List<String> matched_skills;
  public List<String> missing_skills;
  public List<String> suggestions;
  public Map<String, String> target;

  public List<Map<String, Object>> matches;
  public String note;
}
