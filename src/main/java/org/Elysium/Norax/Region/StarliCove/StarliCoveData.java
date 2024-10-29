package org.Elysium.Norax.Region.StarliCove;


import org.Elysium.Norax.Region.RegionData;

public class StarliCoveData implements RegionData {
    @Override
    public String getRegionId() {
        return "i21";
    }

    @Override
    public String getName() {
        return "Starli Cove";
    }

    @Override
    public String getElementalPower() {
        return "Water";
    }

    @Override
    public String getDescription() {
        return "It is a serene coastal area where the waters shimmer under a blanket of stars, featuring vibrant coral reefs, unique marine life, and hidden treasures waiting to be discovered along its shores.";
    }
}
