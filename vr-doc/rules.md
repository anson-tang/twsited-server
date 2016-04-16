 private Vector3 getxyz(int radius,int id)
    {
        
        return radius * getxyz(1f);

        //id = Random.Range(0, SphericalList.Count);
        //return radius * SphericalList[id];
    }
    private Vector3 getxyz(float ratio)
    {
        float x, y, z;
        y = 1f;
        float h = ratio;
        float rand = Random.Range(-h, h);
        y = rand;

        z = Mathf.Sqrt(1 - y * y);
        rand = Random.Range(-z, z);
        z = rand;

        x = Mathf.Sqrt(1 - z * z - y * y);

        rand = Random.Range(-1, 1);
        if (rand != 0)
            return new Vector3(rand * x, y, z);
        else
        {
            return new Vector3(x, y, z);
        }
    }
