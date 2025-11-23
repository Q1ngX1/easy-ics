import { useState } from "react";

/**
 * Hook for managing location and timezone settings
 * Handles: geolocation requests, timezone detection, checkbox states
 */
export function useLocationSettings() {
  const [useLocation, setUseLocation] = useState(false);
  const [useTimezone, setUseTimezone] = useState(false);
  const [locationInfo, setLocationInfo] = useState(null);
  const [timezoneInfo, setTimezoneInfo] = useState(null);

  /**
   * Get user's geolocation via browser API
   */
  const getUserLocation = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error("Geolocation not supported"));
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
          });
        },
        (error) => reject(error)
      );
    });
  };

  /**
   * Get user's timezone
   */
  const getTimezone = () => {
    return {
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      datetime: new Date().toISOString(),
    };
  };

  /**
   * Handle location checkbox change
   */
  const handleLocationChange = (checked) => {
    setUseLocation(checked);
    if (!checked) {
      setLocationInfo(null);
    }
  };

  /**
   * Handle timezone checkbox change
   */
  const handleTimezoneChange = (checked) => {
    setUseTimezone(checked);
    if (checked) {
      setTimezoneInfo(getTimezone());
    } else {
      setTimezoneInfo(null);
    }
  };

  return {
    useLocation,
    useTimezone,
    locationInfo,
    timezoneInfo,
    getUserLocation,
    getTimezone,
    handleLocationChange,
    handleTimezoneChange,
    setLocationInfo,
    setTimezoneInfo,
  };
}
