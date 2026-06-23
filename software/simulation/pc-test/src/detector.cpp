#include "detector.h"

SedentaryDetector::SedentaryDetector(const Config& config)
  : config_(config)
  , state_(VACANT)
  , baseline_angle_(0)
  , debounce_counter_(0)
  , occupied_start_ms_(0)
  , current_ms_(0)
{}

void SedentaryDetector::calibrate(float baseline_angle) {
  baseline_angle_ = baseline_angle;
}

int SedentaryDetector::update(float current_angle) {
  current_ms_ += config_.sample_interval_ms;

  float delta = std::abs(current_angle - baseline_angle_);

  bool likely_occupied = (delta > config_.angle_threshold_occupied);
  bool likely_vacant = (delta < config_.angle_threshold_vacant);

  if (likely_occupied && state_ == VACANT) {
    debounce_counter_++;
    if (debounce_counter_ >= config_.debounce_count) {
      state_ = OCCUPIED;
      occupied_start_ms_ = current_ms_;
      debounce_counter_ = 0;
      return 1;  // 变为有人
    }
  } else if (likely_vacant && state_ == OCCUPIED) {
    debounce_counter_++;
    if (debounce_counter_ >= config_.debounce_count) {
      state_ = VACANT;
      debounce_counter_ = 0;
      return -1;  // 变为无人
    }
  } else {
    debounce_counter_ = 0;
  }

  return 0;  // 无变化
}

unsigned long SedentaryDetector::get_sedentary_minutes() const {
  if (state_ == OCCUPIED && occupied_start_ms_ > 0) {
    return (current_ms_ - occupied_start_ms_) / 60000;
  }
  return 0;
}

bool SedentaryDetector::is_sedentary_alert() const {
  return get_sedentary_minutes() >= config_.sedentary_minutes;
}
