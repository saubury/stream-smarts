package com.vsimon.kafka.streams;

import io.confluent.ksql.function.udf.Udf;
import io.confluent.ksql.function.udf.UdfDescription;

@UdfDescription(name = "anomoly_power", description = "Return anomility score from 0..1 from expected value")

public class AnomolyPower {


    @Udf(description = "Return anomility score from 0..1 from expected value")
    public double anomoly_power(final double hr, final double mwh) {

        double ret = -1;

        if (hr==0) { ret = (mwh-110) / (464-110); }
        if (hr==1) { ret = (mwh-112) / (346-112); }
        if (hr==2) { ret = (mwh-109) / (390-109); }
        if (hr==3) { ret = (mwh-114) / (361-114); }
        if (hr==4) { ret = (mwh-108) / (363-108); }
        if (hr==5) { ret = (mwh-110) / (348-110); }
        if (hr==6) { ret = (mwh-111) / (1954-111); }
        if (hr==7) { ret = (mwh-108) / (2689-108); }
        if (hr==8) { ret = (mwh-107) / (2607-107); }
        if (hr==9) { ret = (mwh-111) / (2120-111); }
        if (hr==10) { ret = (mwh-106) / (2032-106); }
        if (hr==11) { ret = (mwh-107) / (2272-107); }
        if (hr==12) { ret = (mwh-108) / (1639-108); }
        if (hr==13) { ret = (mwh-108) / (1333-108); }
        if (hr==14) { ret = (mwh-109) / (1555-109); }
        if (hr==15) { ret = (mwh-108) / (1458-108); }
        if (hr==16) { ret = (mwh-108) / (2371-108); }
        if (hr==17) { ret = (mwh-108) / (2716-108); }
        if (hr==18) { ret = (mwh-114) / (3296-114); }
        if (hr==19) { ret = (mwh-109) / (3380-109); }
        if (hr==20) { ret = (mwh-108) / (3745-108); }
        if (hr==21) { ret = (mwh-110) / (3381-110); }
        if (hr==22) { ret = (mwh-107) / (2463-107); }
        if (hr==23) { ret = (mwh-112) / (566-112); }

        return ret;
    }
}
