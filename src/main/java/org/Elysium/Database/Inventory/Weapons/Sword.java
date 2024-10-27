package org.Elysium.Database.Inventory.Weapons;

import org.Elysium.Database.Inventory.Inventory;

public class Sword implements Weapon, Inventory {
    private final String itemId;
    private final String name;
    private final String regionOrigin;
    private final String type;
    private int damage;
    private int level;

    public Sword(String itemId, String name, String regionOrigin, String type) {
        this.itemId = itemId;
        this.name = name;
        this.regionOrigin = regionOrigin;
        this.type = type;
        this.damage = 25;
        this.level = 1;
    }

    @Override
    public String getItemId() {
        return itemId;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getRegionOrigin() {
        return regionOrigin;
    }

    @Override
    public String getType() {
        return type;
    }

    @Override
    public String getDamage() {
        return String.valueOf(damage);
    }

    @Override
    public String getLevel() {
        return String.valueOf(level);
    }

    public void upgradeDamage(int additionalDamage) {
        this.damage += additionalDamage;
    }

    public void upgradeLevel() {
        this.level++;
    }
}

