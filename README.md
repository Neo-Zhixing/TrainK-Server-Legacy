近年来，中国的铁路系统发展迅速，高铁逐渐成为人们中近距离跨城出行的主要方式。但是铁道部的国企性质导致他们的信息化系统对用户极度不友好。例如，官方售票网站12306就是饱受诟病的典型。在这样的基础上，一款铁路行程管理系统变得十分重要。中国的民航业，有航旅纵横、飞常准这样优秀的app，去处理行程管理方面的问题；但是铁路行业，还存在这样的市场空白。简单在知乎上搜索“铁路 航旅纵横”，就能看到这样的问题：“为啥高铁没有航旅纵横这样的app” “为啥12306的app这么难用”。可见用户对这样一款铁路行程管理的app，存在很大的需求。

目前铁道部并没有开放公开的api，也不支持第三方app的发展。例如，他们的官方售票网站header上就有这么一行字：目前铁道部没有授权第三方app进行售票活动。但是，铁道部也不限制app等的开发 - 市面上的售票网站，如携程去哪儿，可以随意进行运营。这是由于12306的web api极其简单，缺乏必要的加密措施，使得我们通过爬虫等技术接入12306私有api变的可能。我们即使在TrainK中接入售票的功能，也是通过12306的api，间接向铁路部门提出的，因此不存在特别的法律问题。

目前，市场上存在大量开发好的购票平台（携程去哪儿艺龙等）给我们使用。虽然铁路购票或抢票方面的竞争激烈，但是行程管理app却缺乏竞争，目前提供类似服务的仅有高铁管家一家，且他们不会提供web端服务，仅有android和ios 端app提供服务。他们的功能也偏于单一，还是以售票/抢票为卖点。因此，我们应该把开发的重点放在行程管理和信息查询方面，而不是已经成为红海的售票抢票业务。

## 在这里举几个TrainK可以实现的功能的例子：
* 行程管理：用户扫描车票/导入12306订单（包括直接从12306买的，和从第三方购票网站买的）/直接从TrainK购买车票，添加未来行程。此后，TrainK会自动推送和管理 取票码/进站口/车站位置/正晚点 等信息。需要注意的是，铁路部门没有关于取票码和进站口的api，但是购票后他们会向用户邮箱发送信息。所以我们将会要求用户把12306绑定的邮箱更换为*****@tra.ink的邮箱，然后设置SMTP服务器来收取铁道部发送的邮件。
* 通勤铁路：针对部分跨城上班族的需求（北京-雄安/天津，北京西-北京-北京南-通州，上海-苏州/金山，珠三角城际网络，成绵乐等），我们提供车票订阅功能，每天/每周为用户购买固定车次的车票。
* 铁路地图：把中国的高铁网络，做成类似地铁图一样的交互性地图，方便人们换乘/查看
* 历史晚点：12306仅提供开车前3小时-开车后1小时的正晚点信息供人们查询，但我们可以通过持续不断的查询，获取历史所有正晚点信息，并且通过这些信息为用户提供出行建议。如：您乘坐的列车，过去七天每天都会晚点30分钟到达（普通列车中经常有这样的情况），建议你安排好到达交通，等等。

TrainK前期运营时，会直接对接12306的购票接口，相当于给12306添加一层前端，因此不会产生任何的运营成本。需要承担的成本，只有云主机的租用费用，Redis Postgres数据库，消息队列，CDN流量、对象存储等云服务器的费用。目前阿里云、腾讯云都有针对学生的扶植计划，如果是在校大学生，可以以极低的价格购买服务器。因此，这方面的成本是可以忽略的。票务运营前期将会以包装铁道部12306售票接口的方式进行，后期如果想当票务代理，也可以去与本地的票务代理进行合作。

近年铁道部市场化改革在逐步推进，提升购票体验的工作肯定不会少。例如最近，12306的官方网站就推出了接续换乘，网上订餐，会员积分等功能。因此，铁路行程管理方面app未来的机遇，未来是不会少的。

## What will TrainK do

* Track the status of every single train running on Chinese railroad and provide users with real-time reports and prediction about delays.

* Over time, TrainK will be able to give suggestions to help users choose between trains and avoid the ones with a higher delay possibility using the data accumulated.

* Provide users with a better ticket-booking interface and an easier procedure.

* Enable none-Chinese speakers to book tickets online. For now, the official booking website 12306.cn does not have a multi-language interface; the captcha is an impossible problem for a foreigner. What’s more, you’ll need a Chinese phone number and a Chinese bank account to purchase tickets – they don’t accept Visa, Master Card or American Express. Hopefully, TrainK will be able to deal with all these requirements for none-Chinese users.

## How I’m going to do it

Although 12306.cn doesn’t have a set of public APIs, we do have some APIs scraped from their website. That will make feature 1-3 available.

These APIs don't provide information in a convenient way, since they're for ajax. For example, the API for delays is only available -1 - +3 hours before the train departures. But over time, we can accumulate and intrepret these information, save them in the database, and show them in a straight-forward, user-friendly way.
