package com.futurepath.commands;

import java.util.Scanner;

import com.futurepath.model.CampusProfile;
import com.futurepath.model.MatchRequest;
import com.futurepath.model.MatchResponse;
import com.futurepath.repo.RunRepository;
import com.futurepath.service.MlApiService;
import com.futurepath.util.JsonUtil;
import com.futurepath.util.PdfUtil;

public class AnalyzeCommand implements Command {
  private final MlApiService api = new MlApiService();
  private final RunRepository repo = new RunRepository();

  @Override public String key() { return "1"; }
  @Override public String description() { return "Analyze (Modes A/B/C) and save history (JDBC/SQLite)"; }

  @Override public void run() {
    Scanner sc = new Scanner(System.in);

    MatchRequest req = new MatchRequest();
    req.profile = inputProfile(sc);

    System.out.print("Resume PDF path (empty to paste text): ");
    String pdf = sc.nextLine().trim();
    if (!pdf.isEmpty()) {
      String txt = PdfUtil.extractText(pdf);
      if (txt == null || txt.isBlank()) {
        System.out.println("Could not read PDF text. Paste resume text:");
        req.resume_text = sc.nextLine();
      } else {
        req.resume_text = txt;
      }
    } else {
      System.out.println("Paste resume text (single line is ok):");
      req.resume_text = sc.nextLine();
    }

    if (req.resume_text != null && req.resume_text.length() > 20000) {
      req.resume_text = req.resume_text.substring(0, 20000);
      System.out.println("Note: resume text trimmed to 20000 chars for speed.");
    }

    System.out.print("Target Company (optional): ");
    req.company = sc.nextLine().trim();

    System.out.print("Target Role (optional): ");
    req.role = sc.nextLine().trim();

    MatchResponse res = api.match(req);

    repo.save(JsonUtil.toJson(req), JsonUtil.toJson(res));

    print(res);
  }

  private CampusProfile inputProfile(Scanner sc) {
    CampusProfile p = new CampusProfile();
    System.out.print("Gender (M/F): "); p.gender = sc.nextLine().trim();
    System.out.print("SSC %: "); p.ssc_p = Double.parseDouble(sc.nextLine().trim());
    System.out.print("HSC %: "); p.hsc_p = Double.parseDouble(sc.nextLine().trim());
    System.out.print("HSC Stream (Science/Commerce/Arts): "); p.hsc_s = sc.nextLine().trim();
    System.out.print("Degree %: "); p.degree_p = Double.parseDouble(sc.nextLine().trim());
    System.out.print("Degree Type (Sci&Tech/Comm&Mgmt/Others): "); p.degree_t = sc.nextLine().trim();
    System.out.print("WorkEx (Yes/No): "); p.workex = sc.nextLine().trim();
    System.out.print("E-test %: "); p.etest_p = Double.parseDouble(sc.nextLine().trim());
    System.out.print("Specialisation (Mkt&Fin/Mkt&HR): "); p.specialisation = sc.nextLine().trim();
    System.out.print("MBA %: "); p.mba_p = Double.parseDouble(sc.nextLine().trim());
    return p;
  }

  private void print(MatchResponse r) {
    System.out.println("\n--- RESULT ---");
    System.out.println("Mode: " + r.mode);
    System.out.println("Placement Probability: " + r.placement_probability + "%");

    if ("A".equals(r.mode)) {
      System.out.println("Role Fit Score: " + r.role_fit_score);
      System.out.println("Resume ATS Score: " + r.resume_ats_score);
      System.out.println("Missing Skills: " + r.missing_skills);
      System.out.println("Suggestions: " + r.suggestions);
      if (r.target != null) System.out.println("Target: " + r.target);
    } else {
      System.out.println("Top Matches:");
      if (r.matches != null) {
        for (int i = 0; i < Math.min(10, r.matches.size()); i++) {
          System.out.println(" - " + r.matches.get(i));
        }
      }
      if (r.note != null) System.out.println("Note: " + r.note);
    }
  }
}
