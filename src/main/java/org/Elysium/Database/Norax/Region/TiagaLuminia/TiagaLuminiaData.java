package org.Elysium.Database.Norax.Region.TiagaLuminia;

import org.Elysium.Database.Norax.Region.RegionData;

public class TiagaLuminiaData implements RegionData {
    @Override
    public String getRegionId() {
        return "i10";
    }

    @Override
    public String getName() {
        return "Tiaga Luminia";
    }

    @Override
    public String getElementalPower() {
        return "Light";
    }

    @Override
    public String getDescription() {
        return "A vibrant forest filled with bioluminescent plants and glowing creatures, creating a magical atmosphere.";
    }
}
