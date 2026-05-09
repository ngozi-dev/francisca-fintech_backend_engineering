BEGIN Ride_Matching_Process

    // Step 1: Input Data
    // NECESSITY: We need the start and end points to calculate routes and identify nearby drivers.
    INPUT userLocation
    INPUT destination

    // Step 2: Search for Drivers
    // NECESSITY: Restricting to 5km ensures reasonable pickup times and fuel efficiency for the driver.
    SET searchRadius = 5.0 
    SET availableDrivers = CALL Get_Drivers_Within_Radius(userLocation, searchRadius)
    
    // Sort drivers so the closest one always gets the first opportunity.
    SORT availableDrivers BY distance ASCENDING

    // Step 3: Initial Availability Check
    // NECESSITY: Provides immediate feedback to the user if the service area is currently empty.
    IF availableDrivers IS EMPTY THEN
        DISPLAY "No drivers available in your area. Please try again later."
        EXIT
    END IF

    SET rideMatched = FALSE

    // Step 4: Iterative Request Loop
    // NECESSITY: This handles the "If declined or timed out, find the next nearest" requirement.
    FOR EACH driver IN availableDrivers
        
        // Step 5: Fare Calculation
        // NECESSITY: Pricing transparency is required before the driver accepts the contract.
        SET tripDistance = CALL Calculate_Distance(userLocation, destination)
        SET tripDuration = CALL Estimate_Travel_Time(userLocation, destination)
        SET estimatedFare = (tripDistance * ratePerKm) + (tripDuration * ratePerMin)

        // Step 6: Dispatch Request
        // NECESSITY: This initiates the formal communication with the driver's device.
        SEND_REQUEST(driver, userLocation, destination, estimatedFare)
        
        SET startTime = GET_CURRENT_TIME()
        SET driverResponse = PENDING

        // Step 7: Response Wait Window
        // NECESSITY: A 30s timeout prevents the user from being stuck in limbo if a driver is inactive.
        WHILE (GET_CURRENT_TIME() - startTime < 30 SECONDS)
            driverResponse = GET_DRIVER_RESPONSE(driver)
            
            IF driverResponse IS "ACCEPTED" OR "DECLINED" THEN
                BREAK WHILE
            END IF
        END WHILE

        // Step 8: Handle Response Outcomes
        IF driverResponse == "ACCEPTED" THEN
            // NECESSITY: Confirms the transaction and begins the service phase.
            rideMatched = TRUE
            NOTIFY_USER("Driver found and arriving soon!")
            CALL Start_Live_Tracking(driver, userLocation)
            EXIT FOR // Stop looking for more drivers
        ELSE
            // NECESSITY: If declined or timed out, the loop continues to the next closest driver.
            CONTINUE FOR
        END IF

    END FOR

    // Step 9: Final Fallback
    // NECESSITY: Informs the user if the entire list of nearby drivers was exhausted without an acceptance.
    IF rideMatched == FALSE THEN
        DISPLAY "Drivers are busy or unavailable. Please try again in a few minutes."
    END IF

END Ride_Matching_Process
