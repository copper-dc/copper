package org.Elysium.Utils.Inventory.Weapons;

public abstract class AbstractWeapon implements Weapon {
    protected final String itemId;
    protected final String name;
    protected final String regionOrigin;
    protected final String type;
    protected int damage;
    protected int level;

    public AbstractWeapon(String itemId, String name, String regionOrigin, String type, int damage, int level) {
        this.itemId = itemId;
        this.name = name;
        this.regionOrigin = regionOrigin;
        this.type = type;
        this.damage = damage;
        this.level = level;
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
