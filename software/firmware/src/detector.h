#pragma once

#include <cmath>
#include <cstdint>

class SedentaryDetector {
public:
  enum State { VACANT, OCCUPIED };

  struct Config {
    float angle_threshold_occupied;
    float angle_threshold_vacant;
    int debounce_count;
    int sedentary_minutes;
    int sample_interval_ms;

    Config()
      : angle_threshold_occupied(1.0f)
      , angle_threshold_vacant(0.5f)
      , debounce_count(3)
      , sedentary_minutes(45)
      , sample_interval_ms(2000)
    {}
  };

  explicit SedentaryDetector(const Config& config = Config());

  void calibrate(float baseline_angle);
  int update(float current_angle);
  State get_state() const { return state_; }
  unsigned long get_sedentary_minutes() const;
  bool is_sedentary_alert() const;

private:
  Config config_;
  State state_;
  float baseline_angle_;
  int debounce_counter_;
  unsigned long occupied_start_ms_;
  unsigned long current_ms_;
};
